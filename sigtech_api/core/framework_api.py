import requests

import time

import urllib.parse
from sigtech_api.core.utils import camel_to_snake, snake_to_camel, singlar
from sigtech_api.core.constants import SIGTECH_API_URL


class _Entity:
    def __init__(self, d: dict, name="Entity", api=None, kwargs=None):
        assert isinstance(d, dict)
        self.d = {camel_to_snake(k): v for (k, v) in d.items()}
        self.api_name = name
        self.api = api
        self.kwargs = kwargs

    def __repr__(self):
        return f"{self.api_name}({repr(self.d)})"

    def wait(self, timeout=60, property_name=None):
        session_id = self.kwargs["session_id"]
        t0 = time.monotonic()
        status = "QUEUED"
        while status != "SUCCEEDED":
            resp = FrameworkApi(
                api_key=self.api._api_key,
                url=f"{SIGTECH_API_URL}/sessions/{session_id}/objects/{self.object_id}",
                session=self.api._session
            ).get()

            status = resp.status

            if status == 'FAILED':
                print(resp)
                break

            if property_name is not None and getattr(resp, property_name) is not None:
                status = "SUCCEEDED"

            time.sleep(1)
            t1 = time.monotonic()
            if (t1 - t0) > timeout:
                raise TimeoutError(f"Timeout waiting for object_id={self.object_id}")

    def __getattr__(self, item):
        return self.d[item]


class FrameworkApi:
    def __init__(self, api_key="none", url=SIGTECH_API_URL, session=None):
        self._url = url
        self._api_key = api_key
        self._session = session or requests.Session()
        self._session.headers.update({
            f"Authorization": f"Bearer {api_key}",
        })

    @property
    def namespace(self):
        return self._url.split("/")[-1]

    def create(self, **kwargs):
        obj = {snake_to_camel(k): v for (k, v) in kwargs.items()}
        # print(f"POST {self._url} {obj}")
        resp = self._session.post(self._url, json=obj)
        if resp.status_code != 200:
            # print(resp.text)
            resp.raise_for_status()
        return _Entity(resp.json(), name=singlar(self.namespace), api=self, kwargs=kwargs)

    def list(self):
        # print(f"GET {self._url}")
        resp = self._session.get(self._url)
        if resp.status_code != 200:
            # print(resp.text)
            resp.raise_for_status()
        return [_Entity(o, name=singlar(self.namespace)) for o in resp.json()[self.namespace]]

    def get(self, id='', **kwargs):
        url = f"{self._url}/{id}"
        if kwargs:
            d = {snake_to_camel(k): v for (k, v) in kwargs.items()}
            url += '?' + urllib.parse.urlencode(d)
        # print(f"GET {url}")
        resp = self._session.get(url)
        if resp.status_code != 200:
            # print(resp.text)
            resp.raise_for_status()
        return _Entity(resp.json(), name=singlar(self.namespace), api=self)

    def __getattr__(self, item):
        return FrameworkApi(self._api_key, f"{self._url}/{item}", self._session)
