import base64
import collections
import concurrent.futures
import csv
import datetime as dtm
import logging
import math
import os
import re
import time
from typing import List

from sigtech.api.datasets.common import get_session

logger = logging.getLogger("datasets")


def upload(
    path: str, dataset_id, mode="append", max_part_size=4_000_000, thread_count=8
):
    if not os.path.isfile(path):
        raise ValueError(f"{path} is not a file.")
    if not path.lower().endswith(".csv"):
        raise ValueError("Only csv files are supported")
    if mode not in ["overwrite", "append"]:
        raise ValueError("Mode must be 'overwrite' or 'append'")
    if not os.path.exists(path):
        raise ValueError(f"No file at path: {path}")

    file_size = os.path.getsize(path)
    logger.info(f"Start upload of file: {path}")
    logger.info(f"File size: {get_si_size(file_size)} ({file_size} bytes).")

    if file_size > max_part_size:
        logger.info(
            f"File size is greater than max_part_size={get_si_size(max_part_size)} "
            f"({max_part_size} bytes). "
            f"File will be split into parts for upload."
        )

    schema_new = get_schema(path)
    logger.info("Got schema from CSV.")

    session = get_session()

    # Try to get a dataset by id
    resp = session.get(f"https://api.sigtech.com/ingestion/datasets/")
    resp.raise_for_status()
    assert resp.status_code == 200

    resp = session.get(f"https://api.sigtech.com/ingestion/datasets/{dataset_id}")
    if resp.status_code == 404:

        if not is_valid_dataset_id(dataset_id):
            raise ValueError("")

        # If it doesn't exist, create it
        resp = session.put(
            f"https://api.sigtech.com/ingestion/datasets/{dataset_id}",
            json={
                "name": dataset_id,
                "schema": schema_new,
                "identifier": dataset_id,
                "tags": {"name": dataset_id},
            },
        )
        resp.raise_for_status()
        resp.reason = resp.text
        assert resp.status_code == 201
        obj = resp.json()
        name, dataset_id = obj["name"], obj["id"]
        logger.info(f"Created new dataset. name={name} id={dataset_id}")

    elif resp.status_code == 200:
        obj = resp.json()
        name, dataset_id = obj["name"], obj["id"]
        logger.info(f"Found existing dataset. name={name} id={dataset_id}")
    else:
        raise Exception("")

    resp = session.get(f"https://api.sigtech.com/ingestion/datasets/{dataset_id}")
    resp.raise_for_status()
    assert resp.status_code == 200
    dataset = resp.json()

    existing_schema = dataset["schema"]
    existing_schema_dict = {o["name"]: o["type"] for o in existing_schema}
    logger.info(f"Dataset schema: {existing_schema_dict}")

    check_schema(existing_schema, schema_new)
    # TODO: Patch old schema if new 1 has more columns

    dataset_id = obj["id"]
    logger.info(f"datasetId={dataset_id}")

    resp = session.get(f"https://api.sigtech.com/ingestion/datasets/{dataset_id}/files")
    resp.raise_for_status()
    files = resp.json()
    logger.info(f"{len(files['ids'])} existing files in dataset.")

    if mode == "overwrite":
        logger.info(f"mode={mode}. Deleting all existing files in dataset")
        session.delete(f"https://api.sigtech.com/ingestion/datasets/{dataset_id}/files")
        resp.raise_for_status()
        assert resp.status_code == 200
        logger.info("Done removing existing dataset files")
    elif mode == "append":
        pass
    else:
        raise NotImplementedError("unknown mode")

    csv_parts = get_csv_parts(path, max_part_size=max_part_size)
    logger.info(f"Split CSV into {len(csv_parts)} parts for upload.")

    logger.info(f"Start upload using {thread_count} threads.")
    t0 = time.monotonic()
    part_names = set()
    now = dtm.datetime.now(dtm.timezone.utc).replace(tzinfo=None, microsecond=0)
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
        future_to_part = {}
        for i, part in enumerate(csv_parts, start=1):
            part_name = get_part_name(now, path, i)
            part_names.add(part_name)
            future = executor.submit(
                upload_part, session, dataset_id, i, part_name, part, schema_new
            )
            future_to_part[future] = part_name
        done_count = 0
        for future in concurrent.futures.as_completed(future_to_part):
            part_name = future_to_part[future]
            try:
                key = future.result()
            except Exception as e:
                logger.error(f"Part={part_name} generated an exception: {e}")
                raise
            else:
                logger.info(f"Part={part_name} uploaded with key={key}")
                done_count += 1
            logger.info(f"Uploaded {done_count} of {len(csv_parts)} parts.")
    t1 = time.monotonic()
    logger.info(
        f"Done upload of {len(part_names)} parts. Took {(t1 - t0):.2f} seconds."
    )

    resp = session.get(f"https://api.sigtech.com/ingestion/datasets/{dataset_id}/files")
    resp.raise_for_status()
    files = resp.json()

    file_ids = files["ids"]
    logger.info(f"Done upload of {len(csv_parts)} parts.")
    logger.info(f"Dataset now has {len(file_ids)} files.")
    logger.info(f"Uploaded dataset. DatasetId={dataset_id}.")

    logger.info(
        f"""To load the dataset in the Jupyter research environment run the following code:
    
        import sigtech.platform_tools
        sigtech.platform_tools.get_dataset("{dataset_id}")
        
    """
    )


def get_part_name(timestamp, path, i):
    assert isinstance(timestamp, dtm.datetime)
    assert timestamp.tzinfo is None
    timestamp_str = timestamp.strftime("%Y%m%dT%H%M%SZ")
    assert len(timestamp_str) == 16
    _, filename = os.path.split(path)
    safe_filename = get_safe_name(filename)
    safe_name = f"{timestamp_str}.{safe_filename}.part-{i:09d}"
    return safe_name


def get_safe_name(s):
    safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-."
    s = "".join(c if c in safe_chars else "_" for c in s)
    s = s.strip("_-.")
    return s


def is_valid_dataset_id(s):
    return get_safe_name(s) == s


def upload_part(session, dataset_id, part_index, part_name, part, schema):
    assert isinstance(dataset_id, str)
    assert isinstance(part_index, int)
    assert isinstance(part, bytes)
    logger.info(f"Start upload of part #={part_index} sizeBytes={len(part)}")
    resp = session.post(
        f"https://api.sigtech.com/ingestion/datasets/{dataset_id}/files",
        json={
            "file_id": part_name,
            "file": base64.b64encode(part).decode(),
            "file_format": "csv",
            "upload_format": "base64",
            "tags": {"name": part_name},
            "convert_options": {"column_types": {o["name"]: o["type"] for o in schema}},
        },
    )
    resp.raise_for_status()
    assert resp.status_code in (200, 201)  # 200 if already exists (still overwritten)
    logger.info(f"Done upload of part #={part_index} sizeBytes={len(part)}")
    obj = resp.json()
    key = obj["raw_file_key"]
    return key


def get_schema(path: str):
    assert path.lower().endswith(".csv")
    with open(path, "r") as f:
        dict_reader = csv.DictReader(f)
        headers = dict_reader.fieldnames
        return [{"name": o, "type": "string"} for o in headers]


def check_schema(schema_old, schema_new):
    s_old = {o["name"]: o["type"] for o in schema_old}
    s_new = {o["name"]: o["type"] for o in schema_new}
    if not (set(s_new) <= set(s_old)):
        raise ValueError(
            f"New dataset schema has extra columns: {set(s_new) - set(s_old)} "
            f"versus the existing dataset schema: {s_old}."
        )


def get_csv_parts(path: str, max_part_size=1_000_000) -> List[bytes]:
    # split csv into parts, each with same header
    assert path.lower().endswith(".csv")
    assert max_part_size >= 1
    parts = []
    line_count = 0
    with open(path, "rb") as f:
        header = f.readline()
        if not header.endswith(b"\n"):
            raise ValueError("CSV file does not start with a header.")
        line_count += 1
        part_size = len(header)
        part = [header]
        for i, line in enumerate(f, start=1):
            line_count += 1
            if len(line) + len(header) > max_part_size:
                raise ValueError(
                    f"Row {i} does not fit within max_part_size={max_part_size}"
                )
            if part_size + len(line) > max_part_size:
                parts.append(b"".join(part))
                part_size = len(header)
                part = [header]
            part.append(line)
            part_size += len(line)
        if len(part) > 1:
            part_bytes = b"".join(part)
            parts.append(part_bytes)
        if not parts:
            raise ValueError("Empty CSV file")
        logger.info(f"Read {line_count} lines from file: {path}.")
        return parts


def get_si_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])
