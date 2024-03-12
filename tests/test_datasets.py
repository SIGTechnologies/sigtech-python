import contextlib
import tempfile
import datetime as dtm
import pytest

from sigtech.api.datasets.upload import get_csv_parts, get_part_name, is_valid_dataset_id, get_safe_name


@contextlib.contextmanager
def _temp_csv(content: str):
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".csv") as f:
        f.write(content.encode())
        f.flush()
        yield f


def test_get_parts_windows_endings():
    with _temp_csv(
        ("a,b,c\r\n" "1,2,3\r\n" "4,5,6\r\n" "7,8,9\r\n" "10,11,12\r\n" "13,14,15\r\n")
    ) as f:
        parts = list(get_csv_parts(f.name, max_part_size=32))
    assert parts == [
        b"a,b,c\r\n1,2,3\r\n4,5,6\r\n7,8,9\r\n",
        b"a,b,c\r\n10,11,12\r\n13,14,15\r\n",
    ]


def test_get_parts_unix_endings():
    with _temp_csv(
        ("a,b,c\n" "1,2,3\n" "4,5,6\n" "7,8,9\n" "10,11,12\n" "13,14,15\n")
    ) as f:
        parts = list(get_csv_parts(f.name, max_part_size=32))
    assert parts == [b"a,b,c\n1,2,3\n4,5,6\n7,8,9\n", b"a,b,c\n10,11,12\n13,14,15\n"]


def test_get_parts_unix_endings_no_newline_at_eof():
    with _temp_csv(
        ("a,b,c\n" "1,2,3\n" "4,5,6\n" "7,8,9\n" "10,11,12\n" "13,14,15")
    ) as f:
        parts = list(get_csv_parts(f.name, max_part_size=32))
    assert parts == [b"a,b,c\n1,2,3\n4,5,6\n7,8,9\n", b"a,b,c\n10,11,12\n13,14,15"]


def test_get_parts_large_part_size():
    with _temp_csv(
        ("a,b,c\r\n" "1,2,3\r\n" "4,5,6\r\n" "7,8,9\r\n" "10,11,12\r\n" "13,14,15\r\n")
    ) as f:
        parts = list(get_csv_parts(f.name, max_part_size=100))
    assert parts == [b"a,b,c\r\n1,2,3\r\n4,5,6\r\n7,8,9\r\n10,11,12\r\n13,14,15\r\n"]


def test_get_parts_too_small_part_size():
    with pytest.raises(ValueError):
        with _temp_csv(
            (
                "a,b,c\r\n"
                "1,2,3\r\n"
                "4,5,6\r\n"
                "7,8,9\r\n"
                "10,11,12\r\n"
                "13,14,15\r\n"
            )
        ) as f:
            get_csv_parts(f.name, max_part_size=1)


def test_get_parts_empty_file():
    with pytest.raises(ValueError):
        with _temp_csv("") as f:
            parts = get_csv_parts(f.name, max_part_size=1)
            assert parts == []


def test_get_parts_header_only():
    with pytest.raises(ValueError):
        with _temp_csv(("a,b,c\r\n")) as f:
            get_csv_parts(f.name, max_part_size=1)


def test_part_name():
    now = dtm.datetime(2022, 1, 1, 0, 0, 0)
    assert (
        get_part_name(now, "/test csv 2022-01-01.csv", 0)
        == "20220101T000000Z.test_csv_2022-01-01.csv.part-000000000"
    )
    assert (
        get_part_name(now, "test.csv -", 1) == "20220101T000000Z.test.csv.part-000000001"
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
