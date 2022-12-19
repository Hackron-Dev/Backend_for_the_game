import requests

def test_delete_user():
    response = requests.delete('http://hackron.studio:8000/users', data={'id': '1', 'password': 'test'})
    assert response.status_code == 410