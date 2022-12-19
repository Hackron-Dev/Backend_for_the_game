import requests
from app.utils.constants import Connection

json = {
    "login": "test",
    "password": "test"
}

data = {
    'username': 'test',
    'password': 'test'
}


def test_create_user():
    response = requests.post(f'{Connection.HOST}/users', json=json)
    assert response.status_code == 201


def test_login_user():
    response = requests.post(f'{Connection.HOST}/login', data=data)
    assert response.status_code == 200


def test_delete_user():
    with requests.session() as session:
        response = requests.post(f'{Connection.HOST}/users', json=json)
        if response.status_code == 400:
            assert response.json()['detail'] == 'User with this login already exist'
        else:
            assert response.status_code == 201

        response = session.post(f'{Connection.HOST}/login', data=data)
        assert response.status_code == 200
        token = response.json()['access_token']

        response = session.get(f'{Connection.HOST}/users/login/test')
        assert response.status_code == 200
        id = response.json()['id']

        response = session.delete(f'{Connection.HOST}/users/{int(id)}',
                                  headers={'Authorization': f'Bearer {token}'})

        assert response.status_code == 410
