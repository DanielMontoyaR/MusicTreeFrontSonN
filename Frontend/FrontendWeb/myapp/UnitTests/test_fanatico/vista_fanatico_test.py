from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
import json
import requests

class FanaticoViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.registrar_url = reverse('registrar_fanatico')
        self.login_url = reverse('login_fanatico')
        self.ver_generos_url = reverse('ver_generos')
        
        # Datos de prueba para registro
        self.registro_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'fullname': 'Test User',
            'pais': 'Test Country',
            'avatar': '1',
            'generos[]': ['1', '2']
        }
        
        # Datos de prueba para login
        self.login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        # Mock de respuesta exitosa
        self.mock_success_response = MagicMock()
        self.mock_success_response.status_code = 200
        self.mock_success_response.json.return_value = {
            'success': True,
            'message': 'Operación exitosa'
        }

    # Pruebas para registrar_fanatico
    def test_registrar_fanatico_get(self):
        """Prueba que la vista responde correctamente a GET"""
        response = self.client.get(self.registrar_url)
        self.assertEqual(response.status_code, 200)
        
    @patch('requests.post')
    def test_registrar_fanatico_post_success(self, mock_post):
        """Prueba registro exitoso"""
        mock_post.return_value = self.mock_success_response
        
        response = self.client.post(
            self.registrar_url,
            data=self.registro_data
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['success'])
        
    @patch('requests.post')
    def test_registrar_fanatico_post_duplicate(self, mock_post):
        """Prueba manejo de usuario duplicado"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_post.return_value = mock_response
        
        response = self.client.post(
            self.registrar_url,
            data=self.registro_data
        )
        
        self.assertEqual(response.status_code, 500)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertIn('ya existe', response_data['error'])

    # Pruebas para login_fanatico
    def test_login_fanatico_get(self):
        """Prueba que la vista responde correctamente a GET"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        
    @patch('requests.post')
    def test_login_fanatico_post_success(self, mock_post):
        """Prueba login exitoso"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'token': 'testtoken123',
            'avatar': 1
        }
        mock_post.return_value = mock_response
        
        response = self.client.post(
            self.login_url,
            data=json.dumps(self.login_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['user_data']['token'], 'testtoken123')
        
    @patch('requests.post')
    def test_login_fanatico_post_invalid_credentials(self, mock_post):
        """Prueba manejo de credenciales inválidas"""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            'detail': 'Credenciales inválidas'
        }
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_post.return_value = mock_response
        
        response = self.client.post(
            self.login_url,
            data=json.dumps(self.login_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['error'], 'Credenciales inválidas')

    # Pruebas para ver_generos
    @patch('requests.get')
    def test_ver_generos_success(self, mock_get):
        """Prueba obtención exitosa de géneros"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'id': 1, 'name': 'Rock'},
            {'id': 2, 'name': 'Pop'}
        ]
        mock_get.return_value = mock_response
        
        response = self.client.get(self.ver_generos_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context)
        self.assertEqual(len(response.context['generos']), 2)
        self.assertIsNone(response.context['error'])
        
    @patch('requests.get')
    def test_ver_generos_api_error(self, mock_get):
        """Prueba manejo de error en la API"""
        mock_get.side_effect = requests.exceptions.RequestException("Error de conexión")
        
        response = self.client.get(self.ver_generos_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['generos']), 0)
        self.assertIsNotNone(response.context['error'])