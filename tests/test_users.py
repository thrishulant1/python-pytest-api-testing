# test_users.py
import pytest
from src.api_client import APIClient

@pytest.fixture
def api():
    return APIClient()

def test_list_users(api):
    response = api.get('/api/users')
    assert response.status_code == 200

    data = response.json()
    users = data['data']
    
    assert users, "No users found in the response"
    for user in users:
        assert 'id' in user
        assert 'email' in user

def test_get_single_user(api):
    response = api.get('/api/users/1')
    assert response.status_code == 200

    data = response.json()
    user = data['data']
    
    assert user['id'] == 1
    assert user['email'] == 'george.bluth@reqres.in'

def test_create_user(api):
    data = {
        'name': 'John Doe',
        'job': 'Tester'
    }
    response = api.post('/api/users', data)
    assert response.status_code == 201

    created_user = response.json()
    assert 'id' in created_user
    assert created_user['name'] == 'John Doe'
    assert created_user['job'] == 'Tester'

def test_update_user(api):
    data = {
        'name': 'Updated Name',
        'job': 'Updated Job'
    }
    response = api.put('/api/users/1', data)
    assert response.status_code == 200

    updated_user = response.json()
    assert updated_user['name'] == 'Updated Name'
    assert updated_user['job'] == 'Updated Job'

def test_delete_user(api):
    response = api.delete('/api/users/2')
    assert response.status_code == 204

# Negative Test Cases

def test_user_not_found(api):
    response = api.get('/api/users/1000')  # Assuming user with ID 1000 does not exist
    assert response.status_code == 404

@pytest.mark.skip()
def test_create_user_invalid_data(api):
    invalid_data = {
        'invalid_key': 'Invalid Value'
    }
    response = api.post('/api/users', invalid_data)
    assert response.status_code == 400  # Assuming the API returns a 400 Bad Request for invalid data
    
@pytest.mark.skip()
def test_unauthorized_access(api):
    response = api.get('/api/protected-resource')  # Assuming 'protected-resource' requires authorization
    assert response.status_code == 401  # Assuming the API returns a 401 Unauthorized

# Edge Test Cases

@pytest.mark.skip()
def test_create_user_max_data_size(api):
    data = {
        'name': 'A' * 200,  # Maximum allowed characters for 'name'
        'job': 'B' * 200,  # Maximum allowed characters for 'job'
    }
    response = api.post('/api/users', data)
    assert response.status_code == 201  # Assuming the API accepts such data

def test_user_pagination(api):
    response = api.get('/api/users', params={'page': 2, 'per_page': 5})
    assert response.status_code == 200
    data = response.json()
    users = data['data']
    assert len(users) == 5  # Assuming you requested 5 users per page

def test_concurrent_requests(api):
    import threading

    def make_request():
        response = api.get('/api/users/1')
        assert response.status_code == 200

    threads = []
    for _ in range(10):
        thread = threading.Thread(target=make_request)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
