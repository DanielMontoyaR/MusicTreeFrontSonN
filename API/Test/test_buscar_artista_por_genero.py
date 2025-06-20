def test_filtrar_artistas_exitoso(client):
    response = client.post('/api/filtrar_artistas', json={
        'nombre': 'Slash', 
        'genre_id': 'G-105AD5A53709000000000000', 
        'subgenre_id': [], 
        'limite': '50'})
    assert response.status_code == 200
    

def test_filtrar_artistas_falla_nombre_no_encontrado(client):
    response = client.post('/api/filtrar_artistas', json={
        'nombre': '2Pac', 
        'genre_id': 'G-105AD5A53709000000000000', 
        'subgenre_id': [], 
        'limite': '50'})
    assert response.status_code == 200
    