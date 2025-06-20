# API/Test/test_login.py

def test_login_exitoso(client):
    response = client.post('/api/login_fan', json={
        "username": "JoseA4718",
        "password": "Pass1234"
    })
    assert response.status_code == 200
    assert response.json["authenticated"] is True

def test_login_falla(client):
    response = client.post('/api/login_fan', json={
        "username": "JoseA4718",
        "password": "pass123"
    })
    assert response.status_code == 401
    assert response.json["authenticated"] is False
