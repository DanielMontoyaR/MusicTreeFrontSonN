import json
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
import requests

from ...vistas.vista_artista import registrar_artista, ver_catalogo_artista, buscar_artista_por_genero

class ArtistaViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        #URLs para vistas
        self.registrar_url = reverse('registrar_artista')  #URLs en urls.py
        self.catalogo_url = reverse('ver_catalogo_artista')
        self.buscar_genero_url = reverse('buscar_artista_genero')

        # Datos de prueba
        self.artista_data = {
            "es_banda": "true",
            "nombre": "Artista Test",
            "biografia": "Biografía de prueba",
            "pais": "Chile",
            "anio_desde": "2000",
            "anio_hasta": "",
            "portada": "ImagenDePrueba",
            "generos[]": ["G-105AD5A53709000000000000"],
            "subgeneros[]": []
        }
        
        self.busqueda_data = {
            "nombre": "Test",
            "genre_id": "G-105AD5A53709000000000000",
            "subgenre_id": [],
            "limite": 50
        }

    @patch('requests.post')
    def test_registrar_artista_exitoso(self, mock_post):
        #print("\n\n\n\n -------------------------- test_registrar_artista_exitoso --------------------------")
        # Configura el mock para simular respuesta exitosa
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'success': True}
        mock_post.return_value = mock_response

        response = self.client.post(
            self.registrar_url,
            data=self.artista_data
        )
        print("\nRespuesta completa → test_registrar_artista_exitoso:", response.json())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

    @patch('requests.post')
    def test_registrar_artista_error(self, mock_post):
        # Configura el mock para simular error 400
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {'error': 'Datos inválidos'}
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Bad Request", response=mock_response)
        mock_post.return_value = mock_response

        # Datos vacíos para forzar error (o datos inválidos)
        response = self.client.post(
            self.registrar_url,
            data={},  # O data={'nombre': ''} para error de validación
            content_type='application/json'
        )
        
        print("\nRespuesta completa → test_registrar_artista_error:", response.json())
        
        # Verifica que:
        # 1. El código de estado sea 400
        # 2. success sea False
        # 3. Contenga el mensaje de error
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertIn('error', response_data)

    @patch('requests.get')
    def test_ver_catalogo_artista(self, mock_get):
        # Configura mock para la API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            'ID Artista': '1',
            'Nombre': 'Artista Test',
            'País de Origen': 'Chile',
            'Álbumes Asociados': 2,
            'Fecha y Hora de Registro': '2023-01-01',
            'Años de Actividad': '2000-actualidad',
            'Estado': 'Activo'
        }]
        mock_get.return_value = mock_response

        response = self.client.get(self.catalogo_url)

        # Debug: ver el contenido de la respuesta (opcional)
        #print("\nContenido de la respuesta:", response.content.decode('utf-8'))
        
        # Verificaciones para respuesta HTML
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')
        self.assertIn('artistas', response.context)
        
        # Verifica que los artistas están en el contexto
        artistas = response.context['artistas']
        self.assertEqual(len(artistas), 1)
        self.assertEqual(artistas[0]['nombre'], 'Artista Test')

    @patch('requests.post')
    def test_buscar_artista_por_genero(self, mock_post):
        #print("\n\n\n\n -------------------------- test_buscar_artista_por_genero --------------------------")
        # Configura mock para búsqueda
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            'id': '1',
            'name': 'Artista encontrado',
            'genres': ['Rock']
        }]
        mock_post.return_value = mock_response

        response = self.client.post(
            self.buscar_genero_url,
            data=json.dumps(self.busqueda_data),
            content_type='application/json'
        )

        print("\nRespuesta completa → test_buscar_artista_por_genero:", response.json())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        self.assertIn('artists', response.json())

    @patch('requests.post')
    def test_buscar_artista_sin_resultados(self, mock_post):
        # Configurar mock para simular 404
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Not Found", response=mock_response)
        mock_response.json.return_value = {'error': 'No encontrado'}
        mock_post.return_value = mock_response

        response = self.client.post(
            self.buscar_genero_url,
            data=json.dumps({
                "nombre": "No existe", 
                "genre_id": "G-105AD5A53709000000000000"
            }),
            content_type='application/json'
        )
        
        print("\nRespuesta completa → test_buscar_artista_sin_resultados:", response.json())  # Para debug
        
        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        self.assertFalse(response_data['success'])  # Asegura que success es False
        self.assertIn('error', response_data)