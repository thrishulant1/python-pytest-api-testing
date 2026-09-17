import pytest
from src.api_client import APIClient

@pytest.fixture
def api():
    return APIClient()

@pytest.fixture
def auth_token():
    # Implement logic to obtain an authentication token
    token = "your_auth_token_here"
    return token
