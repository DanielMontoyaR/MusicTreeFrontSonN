def test_crear_genero_exitoso(client):
    response = client.post('/api/create_genres', json={'name': 'PruebaGeneroMusical1', 'description': 'PruebaGeneroMusicalDescription', 'color': '#CD2020', 'creation_year': 2025, 'country_of_origin': 'Croacia', 'average_mode': 0.5, 'bpm_lower': 0, 'bpm_upper': 120, 'dominant_key': '-1', 'typical_volume': -12.0, 'time_signature': '4', 'average_duration': 180, 'is_subgenre': False, 'parent_genre_id': None, 'cluster_id': None})
    assert response.status_code == 201
    

def test_crear_genero_falla_nombre_repetido(client):
    response = client.post('/api/create_genres', json={'name': 'PruebaGeneroMusical', 'description': 'PruebaGeneroMusicalDescription', 'color': '#CD2020', 'creation_year': 2025, 'country_of_origin': 'Croacia', 'average_mode': 0.5, 'bpm_lower': 0, 'bpm_upper': 120, 'dominant_key': '-1', 'typical_volume': -12.0, 'time_signature': '4', 'average_duration': 180, 'is_subgenre': False, 'parent_genre_id': None, 'cluster_id': None})
    assert response.status_code == 500