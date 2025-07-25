
def test_crear_artista_completo_exitoso(client):
    response = client.post('/api/crear_artista_completo', json={'is_band': True, 'nombre': 'MaxGarroMo', 'biografia': 'DanielArtistaPrueba2Descr', 'pais': 'Costa Rica', 'año_desde': '2025', 'año_hasta': 'presente', 'cover_image_path': 'PruebaImage.jpg', 'miembros': [{'nombre': 'Max', 'instrumento': 'Flauta', 'desde': '2025', 'hasta': 'presente', 'is_current': False}], 'albumes': [{'titulo': 'DanielArtistaPrueba2Album', 'año': '2025', 'duration_seconds': '46', 'cover_image_path': 'PruebaImage.jpg'}], 'genre_ids': ['G-F53F82025731000000000000'], 'subgenre_ids': []})
    assert response.status_code == 201
    

def test_crear_artista_completo_falla_nombre_repetido(client):
    response = client.post('/api/crear_artista_completo', json={'is_band': True, 
    'nombre': 'DanielArtistaPrueba2', 
    'biografia': 'DanielArtistaPrueba', 
    'pais': 'Costa Rica', 
    'año_desde': '2024', 
    'año_hasta': 'presente', 
    'cover_image_path': 'PruebaImage.jpg', 
    'miembros': [{'nombre': 'Max', 'instrumento': 'Flauta', 'desde': '2025', 'hasta': 'presente', 'is_current': False}], 
    'albumes': [{'titulo': 'DanielArtistaPrueba2Album', 'año': '2025', 'duration_seconds': '46', 'cover_image_path': 'PruebaImage.jpg'}],
    'genre_ids': ['G-F53F82025731000000000000'], 'subgenre_ids': []})
    assert response.status_code == 400
    
