def test_get_clusters_genres_exitoso(client):
    response = client.get('get_clusters_genero')

    assert response.status_code == 200
    assert response.is_json