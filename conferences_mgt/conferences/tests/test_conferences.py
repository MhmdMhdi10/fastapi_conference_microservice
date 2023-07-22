from fastapi.testclient import TestClient
import time

from main import app

from fastapi_jwt_auth import AuthJWT

client = TestClient(app)

signup_response = client.post(
        "/auth/users",
        json={"username": "test_user", "password": "test_password"},
    )

login_response = client.post(
        "/auth/login",
        json={"username": "test_user", "password": "test_password"},
    )

access_token = login_response.json()['access']


def test_create_conference():
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.post(
        "/conferences/conference",
        headers=headers,
        json={'id': 1,
              'title': 'new_conference',
              'description': 'new_description',
              'start_time': '2023-07-01 12:00:00',
              'end_time': '2023-07-01 13:00:00',
              'Capacity': 30},
    )
    assert response.status_code == 201


def test_get_conferences():
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.get(
        "/conferences/conferences",
        headers=headers,
    )
    assert response.status_code == 200


def test_create_conference_unauthorized():
    response = client.post(
        "/conferences/conference",
        json={'title': 'new_conference',
              'description': 'new_description',
              'start_time': '2023-07-01 12:00:00',
              'end_time': '2023-07-01 13:00:00',
              'Capacity': 30},
    )
    assert response.status_code == 401


def test_create_conference_bad_input():
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.post(
        "/conferences/conference",
        headers=headers,
        json={'titzle': 'new_conference',
              'a': 'new_description',
              'staasrt_time': '2023-07-01 12:00:00',
              'endzxc_time': '2023-07-01 13:00:00',
              'Capaacity': 30},
    )
    assert response.status_code == 422


def test_update_conference():
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.put(
        "/conferences/conferences/1",
        headers=headers,
        json={'id': 102,
              'title': 'new_conference',
              'description': 'new_description',
              'start_time': '2023-07-01 12:00:00',
              'end_time': '2023-07-01 13:00:00',
              'Capacity': 30},
    )
    assert response.status_code == 200


def test_delete_conference():
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.delete(
        "/conferences/conferences/102",
        headers=headers,
    )
    assert response.status_code == 200
