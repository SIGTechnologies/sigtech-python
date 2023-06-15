import requests
import sigtech.api as sig


def test_example():
    assert 1 + 1 == 2


def test_client_setting_defaults():
    assert sig.ClientSettings().SIGTECH_API_WAIT_TIMEOUT == 60

# def test_my_client(mocker):
#     # Create an instance of the client
#     client = FrameworkApi()
#
#     # Create a mock response
#     mock_response = mocker.Mock()
#     mock_response.status_code = 200
#     mock_response.json.return_value = {"result": "success"}
#
#     # Patch the requests.get method to return the mock response
#     mocker.patch.object(requests, 'get', return_value=mock_response)
#
#     # Make the API call using the client
#     response = client.make_api_call()
#
#     # Assert the response from the client
#     assert response == {"result": "success"}
#
#     # Assert that the requests.get method was called with the expected URL
#     requests.get.assert_called_once_with("https://api.example.com/endpoint")
#
#
# def test_my_client(mocker):
#     # Create an instance of the client
#     client = MyClient()
#
#     # Create a mock response
#     mock_response = mocker.Mock()
#     mock_response.status_code = 200
#     mock_response.json.return_value = {"result": "success"}
#
#     # Patch the requests.post method to return the mock response
#     mocker.patch.object(requests, 'post', return_value=mock_response)
#
#     # Define the expected request body
#     expected_body = {
#         "param1": "value1",
#         "param2": "value2"
#     }
#
#     # Make the API call using the client
#     response = client.make_post_call(expected_body)
#
#     # Assert the response from the client
#     assert response == {"result": "success"}
#
#     # Assert that the requests.post method was called with the expected URL and body
#     requests.post.assert_called_once_with("https://api.example.com/endpoint", json=expected_body)
