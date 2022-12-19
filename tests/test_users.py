import requests
from app.utils.constants import Connection

# region Variables
json = {
    "login": "test",
    "password": "test"
}

data = {
    'username': 'test',
    'password': 'test'
}

token = None  # Token for next tests
user_id = None  # user_id for next tests

headers = {'Authorization': f'Bearer {token}'}


# endregion

def test_create_user():
    response = requests.post(f'{Connection.HOST}/users', json=json)
    if response.status_code == 400:
        assert response.json()['detail'] == 'User with this login already exist'
    else:
        assert response.status_code == 201


def test_login_user():
    global token
    response = requests.post(f'{Connection.HOST}/login', data=data)
    token = response.json()['access_token']
    assert response.status_code == 200


def test_get_user_id():
    global user_id
    response = requests.get(f'{Connection.HOST}/users/login/test')
    user_id = response.json()['id']
    assert response.status_code == 200


def test_update_user_balance():
    with requests.session() as session:
        response = session.put(f'{Connection.HOST}/users/{int(user_id)}', json={'balance': 1000}, headers=headers)
        assert response.status_code == 426

        response = session.get(f'{Connection.HOST}/users/{int(user_id)}', headers=headers)
        assert response.status_code == 200
        assert response.json()['balance'] == 1000

        response = session.put(f'{Connection.HOST}/users/{int(user_id)}', json={'balance': 0}, headers=headers)
        assert response.status_code == 426

        response = session.get(f'{Connection.HOST}/users/{int(user_id)}', headers=headers)
        assert response.status_code == 200
        assert response.json()['balance'] == 0


def test_delete_user():
    with requests.session() as session:
        response = requests.post(f'{Connection.HOST}/users', json=json)
        if response.status_code == 400:
            assert response.json()['detail'] == 'User with this login already exist'
        else:
            assert response.status_code == 201

        response = session.delete(f'{Connection.HOST}/users/{int(user_id)}', headers=headers)
        assert response.status_code == 410

        response = session.get(f'{Connection.HOST}/users/{int(user_id)}')
        assert response.status_code == 404