import requests

import time
import logging

import urllib.parse
from sigtech.api.client.utils import snake_to_camel, singlar
from sigtech.api.client.settings import ClientSettings
from sigtech.api.client.response import Response

logger = logging.getLogger(__name__)


class Client:

    def __init__(self, api_key=None, url=None, session=None, _base_url=None):
        self._url = url or ClientSettings().SIGTECH_API_URL
        self._base_url = _base_url or self._url
        self._api_key = api_key or ClientSettings().SIGTECH_API_KEY

        if self._api_key == '':
            raise Exception('Please provide a SigTech API key.')

        self._session = session or requests.Session()
        self._session.headers.update({
            f"Authorization": f"Bearer {api_key}",
        })

    @property
    def namespace(self):
        return self._url.split("/")[-1]

    def create(self, **kwargs):
        obj = {snake_to_camel(k): v for (k, v) in kwargs.items()}
        logger.debug(f"POST {self._url} {obj}")
        resp = self._session.post(self._url, json=obj)
        if resp.status_code != 200:
            logger.error(f"API REQUEST ERROR - {resp.content}")
            resp.raise_for_status()
        return Response(resp.json(), name=singlar(self.namespace), client=self, kwargs=kwargs)

    def list(self):
        logger.debug(f"GET {self._url}")
        resp = self._session.get(self._url)
        if resp.status_code != 200:
            logger.error(f"API REQUEST ERROR - {resp.content}")
            resp.raise_for_status()
        return [Response(o, name=singlar(self.namespace)) for o in resp.json()[self.namespace]]

    def get(self, id='', **kwargs):
        url = f"{self._url}/{id}"
        if kwargs:
            d = {snake_to_camel(k): v for (k, v) in kwargs.items()}
            url += '?' + urllib.parse.urlencode(d)
        logger.debug(f"GET {url}")
        resp = self._session.get(url)
        if resp.status_code != 200:
            logger.error(f"API REQUEST ERROR - {resp.content}")
            resp.raise_for_status()

        return Response(resp.json(), name=singlar(self.namespace), client=self)

    def query_object(self, session_id, object_id):
        resp = Client(
            api_key=self._api_key,
            url=f"{self._base_url}/sessions/{session_id}/objects/{object_id}",
            session=self._session
        ).get()
        return resp

    def wait_for_object_status(self, session_id, object_id, property_name=None, timeout=None):
        timeout = timeout or ClientSettings().SIGTECH_API_WAIT_TIMEOUT
        t0 = time.monotonic()
        status = None
        sleep_count = 1

        pbar = None
        if ClientSettings().SIGTECH_API_WAIT_TIMER:
            from tqdm.auto import tqdm
            waiting_for = property_name or 'task completion'
            pbar = tqdm(total=timeout, dynamic_ncols=True, leave=False)
            pbar.set_description(f'Waiting for {waiting_for} (session_id: {session_id}, object_id: {object_id})')

        while status != "SUCCEEDED":
            resp = self.query_object(session_id, object_id)

            status = resp.status

            if status == 'FAILED':
                logger.debug(f"FAILED TASK {str(resp)}")
                break

            if property_name is not None and getattr(resp, property_name) is not None:
                status = "SUCCEEDED"

            time.sleep(sleep_count)
            t1 = time.monotonic()
            sleep_count = min(max(1, timeout - (t1 - t0)), sleep_count * 2)

            if (t1 - t0) > timeout:
                raise TimeoutError(f"Timeout waiting for object_id={object_id}")

            if pbar is not None:
                pbar.update(int(t1 - t0))

        if pbar is not None:
            pbar.close()

        return resp

    def __getattr__(self, item):
        return Client(self._api_key, f"{self._url}/{item}", self._session, self._base_url)
