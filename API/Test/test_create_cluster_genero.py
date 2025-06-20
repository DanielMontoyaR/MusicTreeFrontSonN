def test_create_cluster_genero_exitoso(client):
    response = client.post('/create_cluster_genero', json={
        'cluster_id': None, 
        'name': 'ClusterPruebaNombre3', 
        'description': 'ClusterPruebaDescripcion', 
        'is_active': True})
    assert response.status_code == 201
    

def test_create_cluster_genero_falla_nombre_repetido(client):
    response = client.post('/create_cluster_genero', json={
        'cluster_id': None, 
        'name': 'ClusterPruebaNombre', 
        'description': 'ClusterPruebaDescripcion', 
        'is_active': True})
    assert response.status_code == 500