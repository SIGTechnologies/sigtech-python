import fnmatch
import os

import pandas as pd
import requests

from sigtech.api.datasets.delete import (
    delete_dataset,
    delete_dataset_file,
    delete_dataset_files,
)
from sigtech.api.datasets.upload import upload


def get_session():
    try:
        token = os.environ["SIGTECH_PLATFORM_TOKEN"]
    except KeyError:
        raise ValueError("SIGTECH_PLATFORM_TOKEN environment variable not set")
    headers = {"Authorization": f"Bearer {token}"}
    session = requests.Session()
    session.headers.update(headers)
    return session


class DatasetDoesNotExist(Exception):
    pass


class FileDoesNotExist(Exception):
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


class DatasetsApi:

    def __init__(self, url="https://api.sigtech.com/ingestion"):
        self.session = get_session()
        self.url = url

    @property
    def datasets(self):
        return DatasetsList(None, self.session, f"{self.url}/datasets")


class DatasetsList(ApiObject):

    def get(self, dataset_id):
        return self[dataset_id]

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.obj[item]
        url = f"{self.url}/{item}"
        resp = self.session.get(url)
        if resp.status_code == 200:
            return Dataset(resp.json(), self.session, f"{self.url}/{item}")
        assert resp.status_code == 404
        raise DatasetDoesNotExist(item)

    @property
    def obj(self):
        if self._obj is not None:
            return self._obj
        x = super().obj
        self._obj = [Dataset(o, self.session, f"{self.url}/{o['id']}") for o in x]
        return self._obj

    def filter(self, pattern):
        obj = [o for o in self.obj if fnmatch.fnmatch(o.id, pattern)]
        return DatasetsList(obj, self.session, self.url)

    def df(self):
        return pd.DataFrame([o.dict() for o in self.obj])

    def upload(
        self,
        path,
        dataset_id,
        mode="append",
        max_part_size=3_800_000,
        thread_count=8,
        encoding="utf8",
    ):
        upload(path, dataset_id, mode, max_part_size, thread_count, encoding)


class Dataset(ApiObject):

    def upload(
        self,
        path,
        mode="append",
        max_part_size=3_800_000,
        thread_count=8,
        encoding="utf8",
    ):
        upload(path, self.id, mode, max_part_size, thread_count, encoding)

    @property
    def id(self):
        return self.obj["id"]

    @property
    def name(self):
        return self.obj["name"]

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def delete(self, dry_run=False):
        return delete_dataset(self.id, dry_run=dry_run)

    def __repr__(self):
        items = (f"{k}={repr(v)}" for k, v in self.dict().items())
        return f"{type(self).__name__}({', '.join(items)})"

    @property
    def files(self):
        return FileList(self.id, None, self.session, f"{self.url}/files")


class FileList(ApiObject):

    def __init__(self, dataset_id, obj, session, url):
        super().__init__(obj, session, url)
        self._dataset_id = dataset_id

    @property
    def dataset_id(self):
        return self._dataset_id

    def filter(self, pattern):
        obj = [o for o in self.obj if fnmatch.fnmatch(o.id, pattern)]
        return FileList(self.dataset_id, obj, self.session, self.url)

    def df(self):
        return pd.DataFrame([o.dict() for o in self.obj])

    def delete(self, thread_count=8, dry_run=False):
        delete_dataset_files(
            self.dataset_id, [o.id for o in self.obj], thread_count, dry_run=dry_run
        )

    @property
    def obj(self):
        if self._obj is not None:
            return self._obj
        x = super().obj["ids"]
        self._obj = [
            File(self.dataset_id, {"id": o}, self.session, f"{self.url}/{o}") for o in x
        ]
        return self._obj

    def get(self, file_id):
        return self[file_id]

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.obj[item]
        resp = self.session.get(f"{self.url}/{item}")
        if resp.status_code == 200:
            return File(
                self.dataset_id, {"id": item}, self.session, f"{self.url}/{item}"
            )
        assert resp.status_code == 404
        raise FileDoesNotExist(item)


class File(ApiObject):

    def __init__(self, dataset_id, obj, session, url):
        super().__init__(obj, session, url)
        self._dataset_id = dataset_id

    @property
    def id(self):
        return self.obj["id"]

    @property
    def dataset_id(self):
        return self._dataset_id

    def dict(self):
        return {
            "dataset_id": self.dataset_id,
            "id": self.id,
        }

    def __repr__(self):
        items = (f"{k}={repr(v)}" for k, v in self.dict().items())
        return f"{type(self).__name__}({', '.join(items)})"

    def delete(self, dry_run=False):
        delete_dataset_file(self.dataset_id, self.id, dry_run=dry_run)
