import requests
from app.utils.constants import Connection


def test_online():
    response = requests.get(f'{Connection.HOST}')
    assert response.status_code == 200
