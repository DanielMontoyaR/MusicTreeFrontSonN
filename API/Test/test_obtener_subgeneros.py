
def test_get_genres_exitoso(client):
    response = client.get('/api/get_subgenres')

    assert response.status_code == 200
    assert response.is_json
