import pytest

from sigtech.api.client.client import Client
from sigtech.api.client.response import Response


def test_client_init(monkeypatch):
    c = Client(api_key="apikey", url="http://test.url")
    assert c._api_key == "apikey"
    assert c._url == "http://test.url"
    monkeypatch.delenv("SIGTECH_API_KEY", raising=False)
    with pytest.raises(ValueError):
        _ = Client("")


def test_create(mocker):
    post_mock = mocker.patch("requests.Session.post", autospec=True)
    post_mock.return_value.status_code = 200
    post_mock.return_value.json.return_value = {"key": "value"}
    c = Client("apikey", "http://test.url")
    r = c.create(key="value")
    assert isinstance(r, Response)
    assert r.key == "value"


def test_list(mocker):
    get_mock = mocker.patch("requests.Session.get", autospec=True)
    get_mock.return_value.status_code = 200
    get_mock.return_value.json.return_value = {"test.url": [{"key": "value"}]}
    c = Client("apikey", "http://test.url")
    r = c.list()
    assert isinstance(r, list)
    assert isinstance(r[0], Response)
    assert r[0].key == "value"


def test_get(mocker):
    get_mock = mocker.patch("requests.Session.get", autospec=True)
    get_mock.return_value.status_code = 200
    get_mock.return_value.json.return_value = {"key": "value"}
    c = Client("apikey", "http://test.url")
    r = c.get("id")
    assert isinstance(r, Response)
    assert r.key == "value"


def test_query_object(mocker):
    get_mock = mocker.patch("requests.Session.get", autospec=True)
    get_mock.return_value.status_code = 200
    get_mock.return_value.json.return_value = {"key": "value"}
    c = Client("apikey", "http://test.url")
    r = c.query_object("sessid", "objid")
    assert isinstance(r, Response)
    assert r.key == "value"
