def test_get_clusters_exitoso(client):
    response = client.get('/api/get_clusters')

    assert response.status_code == 200
    assert response.is_json