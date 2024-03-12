import datetime as dtm
import io

import pytest

from sigtech.api.datasets.upload import (
    get_csv_parts,
    get_part_name,
    get_safe_name,
    get_si_size,
    is_valid_dataset_id,
)


def test_get_parts_windows_endings():
    f = io.BytesIO(b"a,b,c\r\n1,2,3\r\n4,5,6\r\n7,8,9\r\n10,11,12\r\n13,14,15\r\n")
    parts = list(get_csv_parts(f, max_part_size=32))
    assert parts == [
        b"a,b,c\r\n1,2,3\r\n4,5,6\r\n7,8,9\r\n",
        b"a,b,c\r\n10,11,12\r\n13,14,15\r\n",
    ]


def test_get_parts_unix_endings():
    f = io.BytesIO(b"a,b,c\n1,2,3\n4,5,6\n7,8,9\n10,11,12\n13,14,15\n")
    parts = list(get_csv_parts(f, max_part_size=32))
    assert parts == [b"a,b,c\n1,2,3\n4,5,6\n7,8,9\n", b"a,b,c\n10,11,12\n13,14,15\n"]


def test_get_parts_unix_endings_no_newline_at_eof():
    f = io.BytesIO(b"a,b,c\n1,2,3\n4,5,6\n7,8,9\n10,11,12\n13,14,15")
    parts = list(get_csv_parts(f, max_part_size=32))
    assert parts == [b"a,b,c\n1,2,3\n4,5,6\n7,8,9\n", b"a,b,c\n10,11,12\n13,14,15"]


def test_get_parts_large_part_size():
    f = io.BytesIO(b"a,b,c\r\n1,2,3\r\n4,5,6\r\n7,8,9\r\n10,11,12\r\n13,14,15\r\n")
    parts = list(get_csv_parts(f, max_part_size=100))
    assert parts == [b"a,b,c\r\n1,2,3\r\n4,5,6\r\n7,8,9\r\n10,11,12\r\n13,14,15\r\n"]


def test_get_parts_too_small_part_size():
    with pytest.raises(ValueError):
        f = io.BytesIO(
            b"a,b,c\r\n"
            b"1,2,3\r\n"
            b"4,5,6\r\n"
            b"7,8,9\r\n"
            b"10,11,12\r\n"
            b"13,14,15\r\n"
        )
        get_csv_parts(f, max_part_size=1)


def test_get_parts_empty_file():
    with pytest.raises(ValueError):
        with io.BytesIO(b"") as f:
            parts = get_csv_parts(f, max_part_size=1)
            assert parts == []


def test_get_parts_header_only():
    with pytest.raises(ValueError):
        with io.BytesIO(b"a,b,c\r\n") as f:
            get_csv_parts(f, max_part_size=1)


def test_part_name():
    now = dtm.datetime(2022, 1, 1, 0, 0, 0)
    assert (
        get_part_name(now, "/test csv 2022-01-01.csv", 0)
        == "20220101T000000Z.test_csv_2022-01-01.csv.part-000000000"
    )
    assert (
        get_part_name(now, "test.csv -", 1)
        == "20220101T000000Z.test.csv.part-000000001"
    )
    assert (
        get_part_name(now, "green_tripdata_2017-02.parquet", 56716)
        == "20220101T000000Z.green_tripdata_2017-02.parquet.part-000056716"
    )
    assert (
        get_part_name(now, "./green_tripdata_2017-02.parquet", 123456789)
        == "20220101T000000Z.green_tripdata_2017-02.parquet.part-123456789"
    )


def test_is_valid_dataset_id():
    assert is_valid_dataset_id("test.csv") is True
    assert is_valid_dataset_id(".test.csv") is False
    assert is_valid_dataset_id("-_test.csv") is False
    assert is_valid_dataset_id(" test f.csv") is False
    assert is_valid_dataset_id("a") is True
    assert is_valid_dataset_id("a.") is False
    assert is_valid_dataset_id(".a") is False
    assert is_valid_dataset_id(".a.") is False


def test_get_safe_name():
    assert get_safe_name("test.csv") == "test.csv"
    assert get_safe_name(".test.csv") == "test.csv"
    assert get_safe_name("-_test.csv") == "test.csv"


def test_get_si_size():
    assert get_si_size(0) == "0 B"
    assert get_si_size(1024) == "1.0 KiB"
    assert get_si_size(1024 * 1024) == "1.0 MiB"
    assert get_si_size(3.0 * 1024 * 1024) == "3.0 MiB"
    assert get_si_size(26291543) == "25.07 MiB"
    assert get_si_size(26291543, 1000) == "26.29 MB"
