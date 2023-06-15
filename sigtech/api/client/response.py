from sigtech.api.client.utils import camel_to_snake


class Response:
    def __init__(self, d: dict, name="Response", client=None, kwargs=None):
        assert isinstance(d, dict)
        self.d = {camel_to_snake(k): v for (k, v) in d.items()}
        self.api_name = name
        self.client = client
        self.kwargs = kwargs

    def __repr__(self):
        return f"{self.api_name}({repr(self.d)})"

    def __getattr__(self, item):
        return self.d[item]

    def latest_object_response(self):
        assert 'session_id' in self.kwargs
        assert 'object_id' in self.d
        return self.client.query_object(self.kwargs["session_id"], self.object_id)

    def wait_for_object_status(self, property_name=None, timeout=None):
        assert 'session_id' in self.kwargs
        assert 'object_id' in self.d

        session_id = self.kwargs["session_id"]

        if property_name is not None and property_name in self.d:
            return self

        if 'status' in self.d and self.d['status'] == 'SUCCEEDED':
            return self

        response = self.client.wait_for_object_status(session_id, self.object_id,
                                                      property_name=property_name, timeout=timeout)

        if response.status == 'FAILED':
            error_message = response.d.get('error', '')
            raise Exception(
                f'SigTech API Error - session_id : {session_id} - object_id : {self.object_id} - Message : {error_message}')

        return response
