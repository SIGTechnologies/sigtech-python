from unittest.mock import Mock

import pytest

from sigtech.api.client.client import Client
from sigtech.api.client.response import Response
from sigtech.api.version import __version__


def test_client_init(monkeypatch):
    c = Client(api_key="apikey", url="http://test.url")
    assert c._api_key == "apikey"
    assert c._url == "http://test.url"
    monkeypatch.delenv("SIGTECH_API_KEY", raising=False)
    with pytest.raises(ValueError):
        _ = Client("")


def test_create(monkeypatch):
    post_mock = Mock()
    post_mock.return_value.status_code = 200
    post_mock.return_value.json.return_value = {"key": "value"}
    monkeypatch.setattr("requests.Session.post", post_mock)
    c = Client("apikey", "http://test.url")
    r = c.create(key="value")
    assert isinstance(r, Response)
    assert r.key == "value"


def test_list(monkeypatch):
    get_mock = Mock()
    get_mock.return_value.status_code = 200
    get_mock.return_value.json.return_value = {"test.url": [{"key": "value"}]}
    monkeypatch.setattr("requests.Session.get", get_mock)
    c = Client("apikey", "http://test.url")
    r = c.list()
    assert isinstance(r, list)
    assert isinstance(r[0], Response)
    assert r[0].key == "value"


def test_get(monkeypatch):
    get_mock = Mock()
    get_mock.return_value.status_code = 200
    get_mock.return_value.json.return_value = {"key": "value"}
    monkeypatch.setattr("requests.Session.get", get_mock)
    c = Client("apikey", "http://test.url")
    r = c.get("id")
    assert isinstance(r, Response)
    assert r.key == "value"


def test_query_object(monkeypatch):
    get_mock = Mock()
    get_mock.return_value.status_code = 200
    get_mock.return_value.json.return_value = {"key": "value"}
    monkeypatch.setattr("requests.Session.get", get_mock)
    c = Client("apikey", "http://test.url")
    r = c.query_object("sessid", "objid")
    assert isinstance(r, Response)
    assert r.key == "value"


def test_client_version_header():
    c = Client("apikey", "http://test.url")
    assert (
        c._session.headers["Sig-Version"]  # pylint: disable=protected-access
        == __version__
    )
