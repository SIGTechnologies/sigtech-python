from sigtech.api.client.utils import camel_to_snake


class Response:
    def __init__(self, d: dict, name="Response", client=None, kwargs: dict = None):
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

    def latest_object_response(self):
        """
        Query the latest object status response from the client.

        :return: The latest object response.
        """
        if not ("session_id" in self.kwargs and "object_id" in self.d):
            raise ValueError("Both 'session_id' and 'object_id' must be present.")
        return self.client.query_object(self.kwargs["session_id"], self.object_id)

    def wait_for_object_status(self, property_name: str = None, timeout: int = None):
        """
        Wait for the object status to be in a final state or a property to be available.

        :param property_name: The name of the property to wait for, (optional) waits for final state if `None`.
        :param timeout: The maximum amount of time to wait, (optional) defaults to client settings.
        :return: The response data for the final object status.
        """
        if not ("session_id" in self.kwargs and "object_id" in self.d):
            raise ValueError("Both 'session_id' and 'object_id' must be present.")

        session_id = self.kwargs["session_id"]
        object_id = self.object_id

        if property_name is not None and property_name in self.__dict__:
            return self

        if self.status == "SUCCEEDED":
            return self

        response = self.client.wait_for_object_status(
            session_id, object_id, property_name=property_name, timeout=timeout
        )

        if response.status == "FAILED":
            error_message = response.d.get("error", "")
            raise Exception(
                f"SigTech API Error - session_id : {session_id} - object_id : {object_id} - Message : {error_message}"
            )

        return response
