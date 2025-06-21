from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
import json
import requests

class GeneroViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.crear_genero_url = reverse('crear_genero_musica')
        self.importar_generos_url = reverse('importar_generos')
        self.get_clusters_api_url = reverse('get_clusters')
        self.get_genres_api_url = reverse('get_genres')
        
        # Datos de prueba para crear género
        self.genero_data = {
            'name': 'Test Genre',
            'description': 'Test Description',
            'color': '#FFFFFF',
            'creation_year': '2000',
            'country_of_origin': 'Test Country',
            'average_mode': '0.5',
            'bpm_lower': '80',
            'bpm_upper': '120',
            'dominant_key': 'C',
            'typical_volume': '0.8',
            'time_signature': '4/4',
            'average_duration': '180',
            'is_subgenre': 'on',
            'parent_genre_id': '1',
            'cluster_id': '1'
        }
        
        # Mock de respuesta exitosa
        self.mock_success_response = MagicMock()
        self.mock_success_response.status_code = 200
        self.mock_success_response.json.return_value = {
            'success': True,
            'message': 'Género creado exitosamente'
        }

    # Pruebas para crear_genero_musica
    def test_crear_genero_get(self):
        """Prueba que la vista responde correctamente a GET"""
        response = self.client.get(self.crear_genero_url)
        self.assertEqual(response.status_code, 200)
        
    @patch('requests.post')
    def test_crear_genero_post_success(self, mock_post):
        """Prueba creación exitosa de género"""
        mock_post.return_value = self.mock_success_response
        
        response = self.client.post(
            self.crear_genero_url,
            data=self.genero_data
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['success'])
        
    @patch('requests.post')
    def test_crear_genero_post_error(self, mock_post):
        """Prueba manejo de errores al crear género"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {'error': 'Error en la API'}
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_post.return_value = mock_response
        
        response = self.client.post(
            self.crear_genero_url,
            data=self.genero_data
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    # Pruebas para get_clusters (API)
    @patch('requests.get')
    def test_get_clusters_success(self, mock_get):
        """Prueba obtención exitosa de clusters"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'cluster_id': 'C-123', 'name': 'Test Cluster'}
        ]
        mock_get.return_value = mock_response
        
        response = self.client.get(self.get_clusters_api_url)
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['nombre'], 'Test Cluster')
        
    @patch('requests.get')
    def test_get_clusters_fallback(self, mock_get):
        """Prueba que devuelve datos mock cuando la API falla"""
        mock_get.side_effect = requests.exceptions.RequestException("Error de conexión")
        
        response = self.client.get(self.get_clusters_api_url)
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 2)  # 2 items en los datos mock

    # Pruebas para get_genres (API)
    @patch('requests.get')
    def test_get_genres_success(self, mock_get):
        """Prueba obtención exitosa de géneros"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'genre_id': 'G-123', 'name': 'Test Genre'}
        ]
        mock_get.return_value = mock_response
        
        response = self.client.get(self.get_genres_api_url)
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['nombre'], 'Test Genre')
        
    @patch('requests.get')
    def test_get_genres_fallback(self, mock_get):
        """Prueba que devuelve datos mock cuando la API falla"""
        mock_get.side_effect = requests.exceptions.RequestException("Error de conexión")
        
        response = self.client.get(self.get_genres_api_url)
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 2)  # 2 items en los datos mock

    # Pruebas para importar_generos
    def test_importar_generos_get(self):
        """Prueba que la vista responde correctamente a GET"""
        response = self.client.get(self.importar_generos_url)
        self.assertEqual(response.status_code, 200)
        
    @patch('requests.post')
    def test_importar_generos_success(self, mock_post):
        """Prueba importación exitosa de géneros"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'success': True,
            'message': 'Géneros importados exitosamente'
        }
        mock_post.return_value = mock_response
        
        response = self.client.post(
            self.importar_generos_url,
            data=json.dumps({'generos': []}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        
    @patch('requests.post')
    def test_importar_generos_with_errors(self, mock_post):
        """Prueba manejo de errores en la importación"""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            'errores': [
                {'status_code': 500, 'index': 1, 'error': 'Género duplicado'},
                {'status_code': 400, 'index': 2, 'error': 'Datos inválidos'}
            ]
        }
        mock_post.return_value = mock_response
        
        response = self.client.post(
            self.importar_generos_url,
            data=json.dumps({'generos': []}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 500)  # Usa el código de error más severo
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertEqual(len(response_data['errores']), 2)
        
    @patch('requests.post')
    def test_importar_generos_api_error(self, mock_post):
        """Prueba manejo de errores de conexión con la API"""
        mock_post.side_effect = requests.exceptions.RequestException("Error de conexión")
        
        response = self.client.post(
            self.importar_generos_url,
            data=json.dumps({'generos': []}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 502)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])