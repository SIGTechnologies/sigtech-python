import datetime as dtm
from dataclasses import dataclass
from typing import Optional

import pytest

from sigtech.api.jobs import epoch_to_datetime, get_list_by_key, get_list_by_keys


@dataclass
class _A:
    id: int
    name: Optional[str] = None


def test_get_list_by_key():
    l1 = [_A(id=1)]
    assert get_list_by_key(l1, "id", 1) == _A(id=1)
    with pytest.raises(KeyError):
        get_list_by_key(l1, "id", 2)
    l2 = [_A(id=1, name="a"), _A(id=2, name="a"), _A(id=3, name="b")]
    assert get_list_by_key(l2, "id", 1) == _A(id=1, name="a")
    with pytest.raises(ValueError):
        get_list_by_key(l2, "name", "a")
    assert get_list_by_keys(l2, ["id", "name"], "b") == _A(id=3, name="b")


def test_epoch_to_datetime():
    assert epoch_to_datetime(1707920890488) == dtm.datetime(
        2024, 2, 14, 14, 28, 10, 488000
    )
