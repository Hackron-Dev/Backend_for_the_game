import requests

def test_online():
    response = requests.get('http://hackron.studio:8000')
    assert response.status_code == 200
