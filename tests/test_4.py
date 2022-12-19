import requests
from app.utils.constants import Connection

data = {
    'username': 'test',
    'password': 'test'
}


def test_delete_user():
    with requests.session() as session:
        response = session.post(f'{Connection.HOST}/login', data=data)
        token = response.json()['access_token']

        response = session.get(f'{Connection.HOST}/users/login/test')
        id = response.json()['id']

        response = session.delete(f'{Connection.HOST}/users/{int(id)}',
                                  headers={'Authorization': f'Bearer {token}'})

        assert response.status_code == 410
