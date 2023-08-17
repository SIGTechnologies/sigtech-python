from unittest.mock import Mock

import pytest

from sigtech.api.client.response import Response


def test_response_init():
    mock_data = {"object_id": "123", "status": "SUCCEEDED"}
    mock_kwargs = {"session_id": "456"}
    r = Response(mock_data, "TestResponse", None, mock_kwargs)

    assert r.object_id == "123"
    assert r.status == "SUCCEEDED"
    assert r.api_name == "TestResponse"
    assert r.kwargs == mock_kwargs


def test_response_repr():
    mock_data = {"object_id": "123", "status": "SUCCEEDED"}
    mock_kwargs = {"session_id": "456"}
    r = Response(mock_data, "TestResponse", None, mock_kwargs)

    assert repr(r) == "TestResponse({'object_id': '123', 'status': 'SUCCEEDED'})"


def test_latest_object_response():
    mock_data = {"object_id": "123", "status": "SUCCEEDED"}
    mock_kwargs = {"session_id": "456"}
    mock_client = Mock()
    r = Response(mock_data, "TestResponse", mock_client, mock_kwargs)

    r.latest_object_response()
    mock_client.query_object.assert_called_once_with("456", "123")


def test_wait_for_object_status():
    mock_data = {"object_id": "123", "status": "SUCCEEDED"}
    mock_kwargs = {"session_id": "456"}
    mock_client = Mock()
    r = Response(mock_data, "TestResponse", mock_client, mock_kwargs)

    assert r.wait_for_object_status() == r
    assert r.wait_for_object_status("status") == r

    mock_data["status"] = "PENDING"
    r = Response(mock_data, "TestResponse", mock_client, mock_kwargs)

    with pytest.raises(Exception) as e_info:
        mock_client.wait_for_object_status.return_value = Response(
            {"status": "FAILED", "error": "Test error"}, "TestResponse"
        )
        r.wait_for_object_status()
    assert (
        str(e_info.value)
        == "SigTech API Error - session_id : 456 - object_id : 123 - Message : Test"
        " error"
    )
