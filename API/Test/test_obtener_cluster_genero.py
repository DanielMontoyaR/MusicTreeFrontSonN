
def test_obtener_cluster_genero_exitoso(client):
    response = client.post('/get_clusters_genero', json={


    })
    assert response.status_code == 200
    assert response.json["status"] == "success"

def test_obtener_cluster_genero_falla(client):
    response = client.post('/get_clusters_genero', json={
        # Datos faltantes o incorrectos
    })
    assert response.status_code == 401
    assert response.json["status"] == "error"
