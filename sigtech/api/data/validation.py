import logging
import time
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

import pandas as pd
import requests

from sigtech.api.client.response import Response
from sigtech.api.data.utils import BaseRule
from sigtech.api.framework.environment import env

if TYPE_CHECKING:
    # Used at import time only, because of circular dependency
    from sigtech.api import Client

logger = logging.getLogger(__name__)


class FileUploadFailed(Exception):
    pass


class Validation:
    def __init__(self, name: str) -> None:
        project = self._get_or_create(name=name)
        self.project_id = project.project_id

    @property
    def files_client(self) -> "Client":
        return env().client.with_path(f"/validation/projects/{self.project_id}/files")

    @property
    def configs_client(self) -> "Client":
        return env().client.with_path(f"/validation/projects/{self.project_id}/configs")

    @property
    def executions_client(self) -> "Client":
        return env().client.with_path(
            f"/validation/projects/{self.project_id}/executions"
        )

    @staticmethod
    @lru_cache(2048)
    def get_rules_and_transforms() -> Response:
        """
        Get metadata of the DaVe rules and transforms available for validation.
            GET /validation/rules

        :return: A Response object representing the rules resource.
        """

        return env().client.validation.rules.get()

    @staticmethod
    def _get_or_create(name: str) -> Response:
        """
        Get an existing DaVe project.
            GET /validation/projects?projectName=<projectName>
        Or create the project if it doesn't exist:
            POST /validation/projects {"projectName": <name>}

        :param name: The name of the DaVe project.

        :return: A Response object representing the project resource.
        """
        project_res: Optional[Response] = None

        projects_res = env().client.validation.projects.list(project_name=name)

        if len(projects_res) == 1 and projects_res[0].project_name == name:
            project_res = projects_res[0]
            logger.info(f"Fetched existing project '{name}'.")
        else:
            project_res = env().client.validation.projects.create(project_name=name)
            logger.info(f"Created new project '{name}'.")

        return project_res

    def delete(self) -> Response:
        """
        Delete an existing DaVe project.
            DELETE /validation/projects/{project_id}

        :return: A Response object representing the deleted resource.
        """

        return env().client.validation.projects.delete(resource_id=self.project_id)

    def upload_file(self, path: Union[str, Path]) -> Response:
        """
        Upload a .csv or .parquet file to the DaVe project. If file with the same
        filename is already uploaded, this operation overwrites the existing file.
            POST /validation/projects/{project_id}/files/ {"fileName": <file_name>}

        :param path: Path to the file to upload.

        :return: A Response object representing the file resource.
        """

        assert isinstance(path, (str, Path))
        path = Path(path) if isinstance(path, str) else path
        file_name = path.name.lower()

        # Validate dataset format
        assert path.exists()
        if path.name.endswith(".parquet"):
            _ = pd.read_parquet(path)
        elif path.name.endswith(".csv"):
            _ = pd.read_csv(path, header=0)
        else:
            raise NotImplementedError(f"File type {path.name} not supported")

        # Upload dataset
        file_upload_response = self.files_client.create(
            file_name=file_name,
        )
        with path.open(mode="rb") as file:
            aws_response = requests.post(
                url=file_upload_response.upload_url,
                data=file_upload_response.upload_form_data,
                files={"file": file},
                timeout=10,
            )
        if aws_response.status_code != 204:
            raise FileUploadFailed(
                "Failed to upload file to s3 using presigned url. aws_response:"
                f" {aws_response}"
            )

        files_resp = self.files_client.list(file_name=file_name)
        assert len(files_resp) == 1
        assert files_resp[0].file_size_bytes > 0
        return files_resp[0]

    def list_files(self) -> List[Response]:
        """
        Get the list of uploaded files and associated metadata for each.
            GET /validation/projects/{project_id}/files/

        :return: A list of Response objects representing the files resources.
        """
        return self.files_client.list(page_size=1000)

    def validate(self, timeout: int = 300) -> Response:
        """
        Run validation on the uploaded files and get the results.
            POST /validation/projects/{project_id}/executions
            GET /validation/projects/{project_id}/executions/{execution_id}

        :param timeout: The maximum amount of time to wait.

        :return: A Response object representing the execution resource.
        """

        # Start validation
        start_exec_resp = self.executions_client.create()
        logger.debug(f"Execution started successfully: {start_exec_resp}")

        # Poll for results
        get_exec_resp: Optional[Response] = None
        t0: float = time.monotonic()
        sleep_count = 0.2

        while not get_exec_resp or get_exec_resp.status == "RUNNING":
            get_exec_resp = self.executions_client.get(
                resource_id=start_exec_resp.execution_id
            )
            time.sleep(sleep_count)
            t1 = time.monotonic()

            sleep_count = min(max(1, timeout - (t1 - t0)), sleep_count * 2)
            if (t1 - t0) > timeout:
                raise TimeoutError(
                    f"Timeout waiting for execution_id={start_exec_resp.execution_id}"
                )

        return get_exec_resp

    def get_config(self, config_id: str = "latest") -> Response:
        """
        Get the project's config.
            GET /validation/projects/{project_id}/configs/{config_id}

        :param config_id: The id of the config to retrieve.
            Defaults to the latest updated config.

        :return: A Response object representing the config resource.
        """

        return self.configs_client.get(resource_id=config_id)

    def update_config(
        self,
        rules: Optional[List[BaseRule]] = None,
        transforms: Optional[List[BaseRule]] = None,
    ) -> Response:
        """
        Update the project's config.
            POST /validation/projects/{project_id}/configs

        :param rules: The list of rules to update the config with.
            If not specified or set to None, the existing rules are kept.
            If set to an empty list, all existing rules are removed.
        :param transforms: The list of transforms to update the config with.
            If not specified or set to None, the existing transforms are kept.
            If set to an empty list, all existing transforms are removed.

        :return: A Response object representing the resource.
        """

        def _rule_obj_to_dict(rule_obj: BaseRule) -> Dict[str, Any]:
            return {
                "type": rule_obj.__class__.__name__,
                "properties": rule_obj.__dict__,
            }

        update_config_response = self.configs_client.create(
            rules=[_rule_obj_to_dict(r) for r in (rules or [])],
            transforms=[_rule_obj_to_dict(r) for r in (transforms or [])],
        )
        logger.debug(f"Rules updated successfully. {update_config_response}")
        return update_config_response
