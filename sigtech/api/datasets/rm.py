import concurrent.futures
import logging

from sigtech.api.datasets.common import get_session
from sigtech.api.datasets.ls import ls, iter_dataset_file_ids

logger = logging.getLogger("datasets")


def rm(identifier, dry_run=False, thread_count=8):
    to_delete = []
    if "/" in identifier:
        dataset_id, pattern = identifier.split("/", maxsplit=1)
        if "*" in dataset_id:
            raise ValueError("Invalid specifier. Use `dataset/*` or `data*`")
        if pattern:
            logger.info(
                f"Removing files matching pattern: '{pattern}' from dataset: {dataset_id}"
            )
        else:
            logger.info(f"Removing all files in dataset {dataset_id}")
        for file_id in iter_dataset_file_ids(dataset_id, pattern):
            to_delete.append(f"{dataset_id}/{file_id}")
    elif "*" not in identifier:
        dataset_id = identifier
        logger.info(f"Removing dataset {dataset_id}")
        to_delete.append(dataset_id)
    else:
        raise ValueError(
            "Invalid specifier. "
            "Use `dataset/*` to remove files or `dataset` to remove a dataset."
        )
    for identifier in to_delete:
        target = "file" if "/" in identifier else "dataset"
        logger.info(f"Removing {target} {identifier}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
        future_to_identifier = {}
        for identifier in to_delete:
            if "/" in identifier:
                dataset_id, file_id = identifier.split("/", maxsplit=1)
                future = executor.submit(
                    remove_dataset_file, dataset_id, file_id, dry_run=dry_run
                )
            else:
                dataset_id = identifier
                future = executor.submit(remove_dataset, dataset_id, dry_run=dry_run)
            future_to_identifier[future] = identifier
        for future in concurrent.futures.as_completed(future_to_identifier):
            identifier = future_to_identifier[future]
            try:
                future.result()
            except Exception as e:
                logger.error(f"Delete of {identifier} generated an exception: {e}")
                raise


def remove_dataset(dataset_id, dry_run=False):
    session = get_session()
    if dry_run is True:
        logger.info(f"Would delete {dataset_id}")
        return
    resp = session.delete(f"https://api.sigtech.com/ingestion/datasets/{dataset_id}")
    resp.raise_for_status()
    assert resp.status_code == 204
    logger.info(f"Deleted {dataset_id}")


def remove_dataset_file(dataset_id, file_id, dry_run=False):
    session = get_session()
    if dry_run is True:
        logger.info(f"Would delete {dataset_id}/{file_id}")
        return
    resp = session.delete(
        f"https://api.sigtech.com/ingestion/datasets/{dataset_id}/files/{file_id}"
    )
    resp.raise_for_status()
    assert resp.status_code == 204
    print(f"Deleted file {dataset_id}/{file_id}")
