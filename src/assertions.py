import json

def assert_content_type(response, expected_content_type):
    """
    Custom assertion to check the content type of the response.
    """
    assert response.headers.get('Content-Type') == expected_content_type, f"Expected content type {expected_content_type}, but got {response.headers.get('Content-Type')}"

def assert_response_data(response, expected_data):
    """
    Custom assertion to check the response data against expected data.
    """
    response_data = response.json()
    assert response_data == expected_data, f"Expected data {expected_data}, but got {response_data}"
