import logging
from typing import Optional

from sigtech.api.client.response import Response
from sigtech.api.client.utils import SigApiException
from sigtech.api.framework.environment import env

logger = logging.getLogger(__name__)


class FrameworkApiObject:
    """
    A class used to handle API objects within the framework.
    """

    def __init__(self, creation_response: Response) -> None:
        """
        Initialize a FrameworkApiObject with a given creation_response.

        :param creation_response: The creation_response to associate with the object.
        """
        self.creation_response: Response = creation_response
        self._status: Optional[str] = None
        self._name: Optional[str] = None
        env().all_objects.add(self)

    @property
    def api_status(self) -> str:
        """
        Retrieve the status of the API object.

        :return: The status of the API object.
        """
        if self._status != "SUCCEEDED":
            latest_response = self.creation_response.latest_object_response()
            self._status = latest_response.status
        assert isinstance(self._status, str)
        return self._status

    @property
    def api_object_id(self) -> str:
        """
        Retrieve the object id of the API object.

        :return: The object id of the API object.
        """
        assert isinstance(self.creation_response.object_id, str)
        return self.creation_response.object_id

    @property
    def api_session_id(self) -> str:
        """
        Retrieve the session id of the API object.

        :return: The session id of the API object.
        """
        assert isinstance(self.creation_response.session_id, str)
        return self.creation_response.session_id

    @property
    def name(self) -> str:
        """
        Retrieve the name of the API object.

        :return: The name of the API object.
        """
        if self._name is not None:
            return self._name

        try:
            latest_response = self.creation_response.wait_for_object_status(
                property_name="name"
            )
            self._name = latest_response.name
            env().object_register[self._name] = self

        except Exception as e:
            raise SigApiException(f"Error while getting the name: {str(e)}")

        return self._name
