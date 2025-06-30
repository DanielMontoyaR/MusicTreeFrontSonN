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
        self.ver_artista_url = reverse('ver_artista')
        self.rate_artist_url = reverse('rate_artist')

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

        self.mock_artistas = [{
            'ID Artista': '1',
            'Nombre': 'Artista de Prueba',
            'País de Origen': 'Chile',
            'Álbumes Asociados': 3,
            'Fecha y Hora de Registro': '2023-01-01T00:00:00Z',
            'Años de Actividad': '2000-2023',
            'Estado': 'Activo'
        }]

        self.mock_artist_data = {
            'get_artist_profile': {
                'artist': {
                    'name': 'Artista de Prueba',
                    'cover_image_path': 'imagen.jpg',
                    'biography': 'Biografía de prueba',
                    'country_of_origin': 'Chile',
                    'average_rating': 4.5,
                    'rating_count': 10,
                    'activity_years': ['2000-2010', '2015-actualidad'],
                    'genres': [{'name': 'Rock'}, {'name': 'Pop'}],
                    'members': [{'name': 'Miembro 1', 'instrument': 'Guitarra'}],
                    'albums': [{'title': 'Álbum 1', 'year': 2005}],
                    'photos': ['foto1.jpg', 'foto2.jpg'],
                    'comments': [{'user': 'Fan1', 'comment': 'Excelente!'}],
                    'events': [{'date': '2023-12-01', 'location': 'Santiago'}]
                }
            }
        }


        self.rate_data = {
                    'artist_id': 'ART-123',
                    'rating': 5
                }
        
        # Configurar sesión para pruebas que requieren fan_id
        session = self.client.session
        session['fan_id'] = 'FAN-456'
        session.save()

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


    @patch('requests.get')
    def test_ver_catalogo_artista(self, mock_get):
        """Prueba que la vista muestra correctamente el catálogo de artistas"""
        # Configura el mock para simular respuesta exitosa
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_artistas
        mock_get.return_value = mock_response

        # Realiza la petición
        response = self.client.get(self.catalogo_url)

        # Verificaciones
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')
        
        # Verifica que los artistas están en el contexto
        self.assertIn('artistas', response.context)
        print("\nRespuesta completa → test_ver_catalogo_artista:", response.status_code)  # Para debug
        # Verifica la transformación de datos
        artistas = response.context['artistas']
        self.assertEqual(len(artistas), 1)
        self.assertEqual(artistas[0]['nombre'], 'Artista de Prueba')
        self.assertEqual(artistas[0]['pais'], 'Chile')
        
        # Verifica que el template correcto se está usando
        self.assertTemplateUsed(response, 'Artista/ver_catalogo_artista.html')

    @patch('requests.get')
    def test_ver_catalogo_artista_con_error(self, mock_get):
        """Prueba el manejo de errores cuando la API falla"""
        # Configura el mock para simular error
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Error interno")
        mock_get.return_value = mock_response

        # Realiza la petición
        response = self.client.get(self.catalogo_url)
        print("\nRespuesta completa → test_ver_catalogo_artista_con_error:", response.status_code)  # Para debug
        # Verificaciones
        self.assertEqual(response.status_code, 200)  # La vista aún debe responder 200
        self.assertIn('artistas', response.context)
        self.assertEqual(len(response.context['artistas']), 0)  # Lista vacía en caso de error
        self.assertIn('error', response.context)  # Mensaje de error debe estar presente



    @patch('requests.post')
    def test_ver_artista_exitoso(self, mock_post):
        """Prueba que la vista muestra correctamente los datos de un artista"""
        # Configurar mock para la API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_artist_data
        mock_post.return_value = mock_response

        # Realizar petición con parámetro artist_id
        response = self.client.get(
            self.ver_artista_url,
            {'artist_id': 'ART-123'}
        )
        
        print("\nRespuesta completa → test_ver_artista_exitoso:", response.status_code)
        
        # Verificaciones
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')
        self.assertTemplateUsed(response, 'Artista/ver_artista.html')
        
        # Verificar que los datos del artista están en el contexto
        self.assertIn('artist', response.context)
        artist = response.context['artist']
        self.assertEqual(artist['name'], 'Artista de Prueba')
        self.assertEqual(artist['country'], 'Chile')
        self.assertEqual(len(artist['genres']), 2)
        self.assertEqual(artist['rating'], 4.5)
        self.assertIn('fan_id', response.context)  # Verificar que fan_id está en el contexto

    @patch('requests.post')
    def test_ver_artista_sin_id(self, mock_post):
        """Prueba el comportamiento cuando no se proporciona artist_id"""
        response = self.client.get(self.ver_artista_url)
        
        print("\nRespuesta completa → test_ver_artista_sin_id:", response.status_code)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], 'Se requiere un ID de artista')

    @patch('requests.post')
    def test_ver_artista_no_encontrado(self, mock_post):
        """Prueba el manejo de errores cuando el artista no existe"""
        # Configurar mock para simular error 404
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Not Found", response=mock_response)
        mock_post.return_value = mock_response

        response = self.client.get(
            self.ver_artista_url,
            {'artist_id': 'ART-999'}
        )
        
        print("\nRespuesta completa → test_ver_artista_no_encontrado:", response.status_code)
        
        self.assertEqual(response.status_code, 200)  # La vista aún debe responder 200
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], "Artista no encontrado")

    @patch('requests.post')
    def test_rate_artist_exitoso(self, mock_post):
        """Prueba la calificación exitosa de un artista"""
        # Configurar mock para respuesta exitosa
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'success': True, 'message': 'Calificación registrada'}
        mock_post.return_value = mock_response

        response = self.client.post(
            self.rate_artist_url,
            data=json.dumps(self.rate_data),
            content_type='application/json'
        )
        
        print("\nRespuesta completa → test_rate_artist_exitoso:", response.json())
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], 'Calificación registrada exitosamente')

    @patch('requests.post')
    def test_rate_artist_sin_fan_id(self, mock_post):
        """Prueba el comportamiento cuando no hay fan_id en sesión"""
        # Eliminar fan_id de la sesión
        session = self.client.session
        session.pop('fan_id', None)
        session.save()

        response = self.client.post(
            self.rate_artist_url,
            data=json.dumps(self.rate_data),
            content_type='application/json'
        )
        
        print("\nRespuesta completa → test_rate_artist_sin_fan_id:", response.json())
        
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['error'], 'Faltan datos requeridos')

    @patch('requests.post')
    def test_rate_artist_ya_calificado(self, mock_post):
        """Prueba el comportamiento cuando el fanático ya calificó al artista"""
        # Configurar mock para simular que ya existe una calificación
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': 'error',
            'message': 'Ya has calificado a este artista anteriormente',
            'your_rating': 4
        }
        mock_post.return_value = mock_response

        response = self.client.post(
            self.rate_artist_url,
            data=json.dumps(self.rate_data),
            content_type='application/json'
        )
        
        print("\nRespuesta completa → test_rate_artist_ya_calificado:", response.json())
        
        self.assertEqual(response.status_code, 200)  # La API responde 200 incluso en este caso
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertIn('Ya has calificado', response_data['error'])
        self.assertEqual(response_data['your_rating'], 4)

    @patch('requests.post')
    def test_rate_artist_error_api(self, mock_post):
        """Prueba el manejo de errores cuando la API falla"""
        # Configurar mock para simular error 500
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Server Error", response=mock_response)
        mock_post.return_value = mock_response

        response = self.client.post(
            self.rate_artist_url,
            data=json.dumps(self.rate_data),
            content_type='application/json'
        )
        
        print("\nRespuesta completa → test_rate_artist_error_api:", response.json())
        
        self.assertEqual(response.status_code, 500)
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertIn('Error en la API', response_data['error'])

    @patch('requests.post')
    def test_forzar_error_ya_calificado(self, mock_post):
        """Prueba específica para forzar y verificar el error 'Ya has calificado'"""
        print("\n=== Iniciando prueba para forzar error 'Ya has calificado' ===")
        
        # 1. Configurar el mock para simular la respuesta de la API cuando ya existe una calificación
        mock_response = MagicMock()
        mock_response.status_code = 200  # Importante: la API responde con 200 incluso en este caso
        mock_response.json.return_value = {
            'status': 'error',
            'message': 'Ya has calificado a este artista anteriormente con rating 4',
            'your_rating': 4  # El rating anterior que dio el usuario
        }
        mock_post.return_value = mock_response

        # 2. Datos de la solicitud (igual que una calificación normal)
        request_data = {
            'artist_id': 'ART-789',
            'rating': 5  # El nuevo rating que está intentando poner
        }

        # 3. Realizar la petición POST
        response = self.client.post(
            self.rate_artist_url,
            data=json.dumps(request_data),
            content_type='application/json'
        )
        
        # 4. Imprimir toda la respuesta para debug (como solicitaste)
        print("\nRespuesta completa → test_forzar_error_ya_calificado:")
        print("Status Code:", response.status_code)
        print("Contenido JSON:", response.json())
        
        # 5. Verificaciones detalladas
        self.assertEqual(response.status_code, 200)  # La API responde con 200
        
        response_data = response.json()
        
        # Verificar que success es False
        self.assertFalse(response_data['success'])
        
        # Verificar que contiene el mensaje de error específico
        self.assertIn('Ya has calificado', response_data['error'])
        
        # Verificar que incluye el rating anterior
        self.assertIn('con este rating (5)', response_data['error'])  # El nuevo rating que intentó poner
        self.assertEqual(response_data['your_rating'], 4)  # El rating anterior
        
        # Verificar que la estructura completa es correcta
        expected_structure = {
            'success': False,
            'error': 'Ya has calificado a este artista anteriormente con rating 4 con este rating (5)',
            'your_rating': 4
        }
        
        # Comparación más flexible para el mensaje de error
        self.assertEqual(response_data['success'], expected_structure['success'])
        self.assertIn('Ya has calificado', response_data['error'])
        self.assertIn('con este rating (5)', response_data['error'])
        self.assertEqual(response_data['your_rating'], expected_structure['your_rating'])
        
        print("=== Prueba completada con éxito ===")