import concurrent.futures
import logging

from sigtech.api.datasets.common import get_session

logger = logging.getLogger("datasets")


def delete_dataset(dataset_id, dry_run=False):
    session = get_session()
    if dry_run is True:
        logger.info(f"Would delete {dataset_id}")
        return
    resp = None
    for _ in range(10):
        resp = session.delete(
            f"https://api.sigtech.com/ingestion/datasets/{dataset_id}"
        )
        if resp.status_code == 204:
            break
        elif resp.status_code == 502:
            logger.error(f"Received status={resp.status_code}, retrying request...")
            continue
        else:
            resp.raise_for_status()
    resp.raise_for_status()
    logger.info(f"Deleted {dataset_id}")


def delete_dataset_file(dataset_id, file_id, dry_run=False):
    session = get_session()
    if dry_run is True:
        logger.info(f"Would delete {dataset_id}/{file_id}")
        return
    resp = session.delete(
        f"https://api.sigtech.com/ingestion/datasets/{dataset_id}/files/{file_id}"
    )
    resp.raise_for_status()
    assert resp.status_code == 204
    logger.info(f"Deleted file {dataset_id}/{file_id}")


def delete_dataset_files(dataset_id, file_ids, thread_count=8, dry_run=False):
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
        future_to_identifier = {}
        for file_id in file_ids:
            future = executor.submit(
                delete_dataset_file, dataset_id, file_id, dry_run=dry_run
            )
            future_to_identifier[future] = file_id
        for future in concurrent.futures.as_completed(future_to_identifier):
            file_id = future_to_identifier[future]
            try:
                future.result()
            except Exception as e:
                logger.error(f"Delete of {file_id} generated an exception: {e}")
                raise
