
def test_get_artists_exitoso(client):
    response = client.get('/api/artists_view')

    assert response.status_code == 200
    assert response.is_json