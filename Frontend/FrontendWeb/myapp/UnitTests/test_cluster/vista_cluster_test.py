from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
import requests

class ClusterViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.crear_url = reverse('crear_cluster')
        self.get_cluster_url = reverse('get_clusters')  # Nombre exacto de urls.py
        
        # Datos de prueba
        self.cluster_data = {
            'cluster_id': 'C-TEST123',
            'name': 'Cluster Test',
            'description': 'Descripción de prueba',
            'is_active': 'true'
        }
        
        self.mock_clusters = [{
            'cluster_id': 'C-TEST123',
            'name': 'Cluster Test',
            'description': 'Descripción de prueba',
            'is_active': True
        }]

    @patch('requests.post')
    def test_crear_cluster_exitoso(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'message': 'Cluster creado'}
        mock_post.return_value = mock_response

        response = self.client.post(self.crear_url, data=self.cluster_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['success'])

    @patch('requests.post')
    def test_crear_cluster_error_duplicado(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {'error': 'Cluster ya existe'}
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_post.return_value = mock_response

        response = self.client.post(self.crear_url, data=self.cluster_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('ya existe', response.context['error'])

    @patch('requests.post')
    def test_crear_cluster_error_api(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException("Error de conexión")
        response = self.client.post(self.crear_url, data=self.cluster_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)
