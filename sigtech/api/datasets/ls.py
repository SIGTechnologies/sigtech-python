import fnmatch
import logging

from sigtech.api.datasets.common import get_session

logger = logging.getLogger("datasets")


def ls(identifier=None):
    if identifier is None:
        logger.info(f"Listing all datasets")
        for dataset_id in iter_dataset_ids():
            yield dataset_id
        return
    elif "/" in identifier:
        dataset_id, pattern = identifier.split("/", maxsplit=1)
        if "*" in dataset_id:
            raise ValueError("Invalid specifier. Use `dataset/*` or `data*`")
        if pattern:
            logger.info(
                f"Listing files matching pattern: '{pattern}' in dataset: {dataset_id}"
            )
        else:
            logger.info(f"Listing all files in dataset {dataset_id}")
        for file_id in iter_dataset_file_ids(dataset_id, pattern):
            yield f"{dataset_id}/{file_id}"
    elif "*" not in identifier:
        dataset_id = identifier
        logger.info(f"Listing all files in dataset: {dataset_id}")
        for file_id in iter_dataset_file_ids(dataset_id):
            yield f"{dataset_id}/{file_id}"
    else:
        dataset_id = identifier
        logger.info(f"Listing datasets matching pattern: '{dataset_id}'")
        yield from iter_dataset_ids(pattern=identifier)


def iter_dataset_ids(pattern=None):
    session = get_session()
    resp = session.get(f"https://api.sigtech.com/ingestion/datasets/")
    resp.raise_for_status()
    assert resp.status_code == 200
    for o in resp.json():
        if (not pattern) or fnmatch.fnmatch(o["id"], pattern):
            yield o["id"]


def iter_dataset_file_ids(dataset_id: str, pattern=None):
    session = get_session()
    resp = session.get(f"https://api.sigtech.com/ingestion/datasets/{dataset_id}/files")
    resp.raise_for_status()
    assert resp.status_code == 200
    for o in resp.json()["ids"]:
        if (not pattern) or fnmatch.fnmatch(o, pattern):
            yield o
