import requests
from app.utils.constants import Connection

data = {
    "login": "test",
    "password": "test"
}


def test_create_user():
    response = requests.post(f'{Connection.HOST}/users', json={'login': 'test', 'password': 'test'})
    assert response.status_code == 201
