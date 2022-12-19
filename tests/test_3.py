import requests
from app.utils.constants import Connection

data = {
    'username': 'test',
    'password': 'test'
}


def test_login():
    response = requests.post(f'{Connection.HOST}/login', data=data)
    assert response.status_code == 200
