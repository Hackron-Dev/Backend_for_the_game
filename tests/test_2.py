import requests

def test_create_user():
    response = requests.post('http://hackron.studio:8000/users', data={'login': 'test', 'password': 'test'})
    assert response.status_code == 201