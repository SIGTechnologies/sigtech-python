import base64
import concurrent.futures
import datetime as dtm
import logging
import math
import os
import time
from typing import IO, List

import pandas as pd

from sigtech.api.datasets.common import get_session
from sigtech.api.datasets.delete import delete_dataset

logger = logging.getLogger("datasets")


def upload(
    path: str,
    dataset_id,
    mode="append",
    max_part_size=3_800_000,
    thread_count=8,
    encoding="utf8",
):
    if not os.path.exists(path):
        raise ValueError(f"No file at path: {path}")
    if not os.path.isfile(path):
        raise ValueError(f"{path} is not a file.")
    if not path.lower().endswith(".csv"):
        raise ValueError("Only csv files are supported")
    if mode not in ["overwrite", "append"]:
        raise ValueError("Mode must be 'overwrite' or 'append'")

    if mode == "overwrite":
        delete_dataset(dataset_id)
        logger.info("Done removing existing dataset files")
    elif mode == "append":
        pass
    else:
        raise NotImplementedError("unknown mode")

    file_size = os.path.getsize(path)
    logger.info(f"Start upload of file: {path}")
    logger.info(f"File size: {get_si_size(file_size)} ({file_size} bytes).")

    if file_size > max_part_size:
        logger.info(
            f"File size is greater than max_part_size={get_si_size(max_part_size)} "
            f"({max_part_size} bytes). "
            f"File will be split into parts for upload."
        )

    csv_schema = get_schema(path, encoding=encoding)
    csv_schema_dict = {o["name"]: o["type"] for o in csv_schema}
    logger.info(f"Got schema from CSV: {csv_schema_dict}")

    session = get_session()

    # Get existing dataset or create new one
    resp = session.get(f"https://api.sigtech.com/ingestion/datasets/{dataset_id}")
    if resp.status_code == 404:
        if not is_valid_dataset_id(dataset_id):
            raise ValueError(f"Invalid dataset_id: {dataset_id}")

        # If it doesn't exist, create it
        resp = session.put(
            f"https://api.sigtech.com/ingestion/datasets/{dataset_id}",
            json={
                "name": dataset_id,
                "schema": csv_schema,
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
    csv_schema_dict = {o["name"]: o["type"] for o in existing_schema}
    logger.info(f"Existing dataset schema: {csv_schema_dict}")

    check_schema(existing_schema, csv_schema)
    # TODO: Patch old schema if new 1 has more columns

    dataset_id = obj["id"]
    logger.info(f"datasetId={dataset_id}")

    with open(path, "rb") as f:
        csv_parts = get_csv_parts(f, max_part_size=max_part_size)
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
                upload_part,
                session,
                dataset_id,
                i,
                part_name,
                part,
                csv_schema,
                encoding=encoding,
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
                logger.info(f"Created file file_id={part_name} uploaded with key={key}")
                done_count += 1
            logger.info(f"Uploaded {done_count} of {len(csv_parts)} parts.")
    t1 = time.monotonic()
    logger.info(
        f"Done upload of {len(part_names)} parts. Took {(t1 - t0):.2f} seconds."
    )
    logger.info(f"Done upload of {len(csv_parts)} parts.")
    logger.info(f"Uploaded dataset. DatasetId={dataset_id}.")
    logger.info(
        f"""To load the dataset in the Jupyter research environment run this code:

        from sigtech.framework.infra.platform import data_tools
        data_tools.get_dataset("{dataset_id}")

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


def is_valid_dataset_id(s):
    return get_safe_name(s) == s


def upload_part(
    session, dataset_id, part_index, part_name, part, schema, encoding="utf8"
):
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
            "read_options": {"encoding": encoding},
            "convert_options": {"column_types": {o["name"]: o["type"] for o in schema}},
        },
    )
    resp.raise_for_status()
    assert resp.status_code in (200, 201)  # 200 if already exists (still overwritten)
    logger.info(f"Done upload of part #={part_index} sizeBytes={len(part)}")
    obj = resp.json()
    key = obj["raw_file_key"]
    return key


def get_schema(path, encoding):
    assert path.lower().endswith(".csv")
    logger.info(f"Reading columns from csv file: {path}.")
    try:
        columns = pd.read_csv(path, encoding=encoding).columns.tolist()
    except UnicodeDecodeError:
        logger.error("cannot decode the file. Might need to specify an encoding.")
        raise
    return [{"name": o, "type": "string"} for o in columns]


def check_schema(schema_old, schema_new):
    s_old = {o["name"]: o["type"] for o in schema_old}
    s_new = {o["name"]: o["type"] for o in schema_new}
    if not (set(s_new) <= set(s_old)):
        raise ValueError(
            f"\nExisting schema: {s_old} \n"
            f"New schema: {s_new} \n"
            f"New dataset schema has extra columns: {set(s_new) - set(s_old)} "
            f"versus the existing dataset schema: {s_old}."
        )


def get_csv_parts(f: IO[bytes], max_part_size=1_000_000) -> List[bytes]:
    # split csv into parts, each with same header
    assert max_part_size >= 1
    parts = []
    line_count = 0
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
    logger.info(f"Read {line_count} lines from file.")
    return parts


def get_si_size(size_bytes, base=1024):
    if size_bytes == 0:
        return "0 B"
    size_name = {
        1000: ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"),
        1024: ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"),
    }[base]
    i = int(math.log(size_bytes, base))
    p = math.pow(base, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


def get_safe_name(s):
    safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-."
    s = "".join(c if c in safe_chars else "_" for c in s)
    s = s.strip("_-.")
    return s
