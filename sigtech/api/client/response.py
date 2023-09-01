import json
from typing import TYPE_CHECKING, Any, Dict, Optional

from sigtech.api.client.utils import SigApiException, camel_to_snake

if TYPE_CHECKING:
    # Used at import time only, because of circular dependency
    from sigtech.api.client.client import Client


class Response:
    def __init__(
        self,
        d: Dict[str, Any],
        name="Response",
        client: Optional["Client"] = None,
        kwargs: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize Response class to hold API response data.

        :param d: Input dictionary from API response.
        :param name: Name of the API response, (optional) defaults to 'Response'.
        :param client: API client instance, (optional) defaults to None.
        :param kwargs: Additional arguments, (optional) defaults to None.
        """
        if not isinstance(d, dict):
            raise TypeError("d must be a dictionary.")
        self.d = {camel_to_snake(k): v for (k, v) in d.items()}
        self.__dict__.update(self.d)
        self.api_name = name
        self.client = client
        self.kwargs = kwargs

    def __repr__(self):
        return f"{self.api_name}({repr(self.d)})"

    def __str__(self):
        try:
            return json.dumps(self.d, indent=2)
        except TypeError as e:
            return f"Error: Unable to serialize data ({str(e)})"

    def latest_object_response(self):
        """
        Query the latest object status response from the client.

        :return: The latest object response.
        """
        if "session_id" not in self.kwargs or "object_id" not in self.d:
            raise ValueError("Both 'session_id' and 'object_id' must be present.")
        return self.client.query_object(self.kwargs["session_id"], self.object_id)

    def wait_for_object_status(
        self, property_name: Optional[str] = None, timeout: Optional[int] = None
    ):
        """
        Wait for the object status to be in a final state or a property to be available.

        :param property_name: The name of the property to wait for.
            (optional; waits for final state if `None`).
        :param timeout: The maximum amount of time to wait.
            (optional; defaults to client settings).
        :return: The response data for the final object status.
        """
        assert self.kwargs and self.d
        if "session_id" not in self.kwargs or "object_id" not in self.d:
            raise ValueError("Both 'session_id' and 'object_id' must be present.")

        session_id = self.kwargs["session_id"]
        object_id = self.object_id

        if property_name is not None and property_name in self.__dict__:
            return self

        if self.status == "SUCCEEDED":
            return self

        assert self.client is not None
        response = self.client.wait_for_object_status(
            session_id, object_id, property_name=property_name, timeout=timeout
        )

        if response.status == "FAILED":
            error_message = response.d.get("error", "")
            raise SigApiException(
                f"SigTech API Error - session_id : {session_id} - object_id :"
                f" {object_id} - Message : {error_message}"
            )

        return response

    def __getattr__(self, name):
        raise AttributeError(
            f"'{repr(self)}' Response object has no attribute '{name}'"
        )
