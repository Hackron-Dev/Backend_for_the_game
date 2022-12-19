import requests


def test_login():
    response = requests.post('http://hackron.studio:8000/login', data={'login': 'test', 'password': 'test'})
    assert response.status_code == 200