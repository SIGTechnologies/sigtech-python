import datetime as dtm
import io
import json
import logging
import os
from collections import defaultdict
from functools import lru_cache

import pandas as pd
import requests

logger = logging.getLogger("jobs")


def get_session():
    try:
        token = os.environ["SIGTECH_PLATFORM_TOKEN"]
    except KeyError:
        raise ValueError("SIGTECH_PLATFORM_TOKEN environment variable not set")
    headers = {"Authorization": f"Bearer {token}"}
    session = requests.Session()
    session.headers.update(headers)
    return session


def epoch_to_datetime(t):
    return dtm.datetime.fromtimestamp(t / 1000.0)


def get_list_by_keys(a, keys, value):
    for key in keys:
        try:
            return get_list_by_key(a, key, value)
        except KeyError:
            pass
    raise KeyError(value)


def get_list_by_key(a, key, value):
    m = defaultdict(list)
    for o in a:
        m[getattr(o, key)].append(o)
    items = m[value]
    if len(items) == 0:
        raise KeyError(value)
    elif len(items) == 1:
        return items[0]
    else:
        raise ValueError(
            f"Multiple items with {key}: '{value}'. Use id instead. {items}"
        )


class JobDoesNotExist(Exception):
    pass


class RunDoesNotExist(Exception):
    pass


class OutputDoesNotExist(Exception):
    pass


class OutputFormatDoesNotExist(Exception):
    pass


class ApiObject:
    def __init__(self, obj, session, url):
        self._obj = obj
        self.session = session
        self.url = url

    def __repr__(self):
        return repr(self.obj)

    def __iter__(self):
        return iter(self.obj)

    def __len__(self):
        return len(self.obj)

    @property
    def obj(self):
        if self._obj is not None:
            return self._obj
        resp = self.session.get(self.url)
        resp.raise_for_status()
        obj = resp.json()
        self._obj = obj
        return self._obj


class JobsApi:

    def __init__(self, url="https://api.sigtech.com/extraction"):
        self.session = get_session()
        self.url = url

    @property
    def jobs(self):
        return JobList(None, self.session, f"{self.url}/jobs")


class JobList(ApiObject):

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.obj[item]
        url = f"{self.url}/{item}"
        resp = self.session.get(url)
        if resp.status_code == 200:
            return Job(resp.json(), self.session, f"{self.url}/{item}")
        assert resp.status_code == 404
        try:
            obj = get_list_by_keys(self.obj, ["name"], item)
        except KeyError:
            raise JobDoesNotExist(item)
        return obj

    def get(self, job_id):
        return self[job_id]

    @property
    def obj(self):
        if self._obj is not None:
            return self._obj
        self._obj = [
            Job(o, self.session, f"{self.url}/{o['flow_id']}") for o in super().obj
        ]
        return self._obj

    def df(self):
        return pd.DataFrame([o.dict() for o in self.obj])


class Job(ApiObject):

    @property
    def id(self):
        return self.obj["flow_id"]

    @property
    def name(self):
        return self.obj["flow_name"]

    @property
    def created_at(self):
        return epoch_to_datetime(self.obj["ts_epoch"])

    def dict(self):
        return {
            "name": self.name,
            "id": self.id,
            "created_at": self.created_at,
        }

    def __repr__(self):
        items = (f"{k}={repr(v)}" for k, v in self.dict().items())
        return f"{type(self).__name__}({', '.join(items)})"

    @property
    def runs(self):
        return RunList(None, self.session, f"{self.url}/runs")


class RunList(ApiObject):

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.obj[item]
        url = f"{self.url}/{item}"
        resp = self.session.get(url)
        if resp.status_code == 200:
            return Run(resp.json(), self.session, f"{self.url}/{item}")
        assert resp.status_code == 404
        raise RunDoesNotExist(item)

    def get(self, run_id):
        return self[run_id]

    @property
    def obj(self):
        if self._obj is not None:
            return self._obj
        self._obj = [
            Run(o, self.session, f"{self.url}/{o['run_id']}") for o in super().obj
        ]
        return self._obj

    def df(self):
        return pd.DataFrame([o.dict() for o in self.obj])

    @property
    def latest(self):
        return Run(None, self.session, f"{self.url}/latest")


class Run(ApiObject):

    @property
    def id(self):
        return self.obj["run_id"]

    @property
    def created_at(self):
        return epoch_to_datetime(self.obj["ts_epoch"])

    def dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
        }

    def __repr__(self):
        items = (f"{k}={repr(v)}" for k, v in self.dict().items())
        return f"{type(self).__name__}({', '.join(items)})"

    @property
    def outputs(self):
        return OutputList(None, self.session, f"{self.url}/outputs")


class OutputList(ApiObject):

    def df(self):
        return pd.DataFrame([o.dict() for o in self.obj])

    @property
    def obj(self):
        if self._obj is not None:
            return self._obj

        self._obj = [
            Output(o, self.session, f"{self.url}/{o['artifact_name']}")
            for o in super().obj
        ]
        return self._obj

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.obj[item]
        resp = self.session.get(f"{self.url}/{item}/info")
        if resp.status_code == 200:
            return Output(resp.json(), self.session, f"{self.url}/{item}")
        assert resp.status_code == 404
        raise OutputDoesNotExist(item)

    def get(self, output_id):
        return self[output_id]


class Output(ApiObject):

    def __init__(self, obj, session, url):
        super().__init__(obj, session, url)

    @property
    def name(self):
        return self.obj["artifact_name"]

    @property
    def created_at(self):
        return epoch_to_datetime(self.obj["ts_epoch"])

    def dict(self):
        return {
            "name": self.name,
            "created_at": self.created_at,
        }

    def __repr__(self):
        items = (f"{k}={repr(v)}" for k, v in self.dict().items())
        return f"{type(self).__name__}({', '.join(items)})"

    def _get_format_url(self, format):
        assert self.url.endswith(self.name)
        url = self.url.removesuffix(self.name)
        return f"{url}_artifacts.{self.name}.{format}"

    @lru_cache()
    def json(self):
        url = self._get_format_url("gzip+json")
        resp = self.session.get(url)
        if resp.status_code == 404:
            raise OutputFormatDoesNotExist(
                f"json format not available for output: {self.name}"
            )
        resp.raise_for_status()
        return json.loads(resp.content)

    @lru_cache()
    def df(self):
        url = self._get_format_url("parquet-snappy")
        resp = self.session.get(url)
        if resp.status_code == 404:
            raise OutputFormatDoesNotExist(
                f"parquet format not available for output: {self.name}"
            )
        resp.raise_for_status()
        content = resp.content
        f = io.BytesIO(content)

        f.seek(0)
        try:
            return pd.read_parquet(f)
        except Exception as e:
            logger.error(
                f"Error during pandas.read_parquet(): {e}. "
                f"Using pyarrow.parquet.read_table() instead."
            )

        import pyarrow.parquet  # type: ignore

        f.seek(0)
        t = pyarrow.parquet.read_table(f, use_pandas_metadata=False)
        return pd.DataFrame(t.to_pydict())
