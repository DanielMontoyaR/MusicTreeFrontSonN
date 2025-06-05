
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from flask import Flask, jsonify, render_template
#from flask_cors import CORS  # Importa el módulo CORS
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests



@csrf_exempt
def registrar_artista(request):
    ruta_template = "Artista/registrar_artista.html"
    
    if request.method == 'GET':
        return render(request, ruta_template)
    
    elif request.method == 'POST':
        try:
            # Construimos el data igual que en tu ejemplo
            data = {
                'is_band': request.POST.get('es_banda', 'false') == 'true',
                'nombre': request.POST.get('nombre'),
                'biografia': request.POST.get('biografia'),
                'pais': request.POST.get('pais'),
                'año_desde': request.POST.get('anio_desde'),
                'año_hasta': request.POST.get('anio_hasta'),
                'cover_image_path': request.FILES.get('portada').name if request.FILES.get('portada') else None,
                'miembros': [],
                'albumes': [],
                'genre_ids': [],
                'subgenre_ids': [],
            }

            # Procesar miembros dinámicos
            i = 1
            while f'MemberName{i}' in request.POST:
                data['miembros'].append({
                    'nombre': request.POST.get(f'MemberName{i}'),
                    'instrumento': request.POST.get(f'MemberInstrument{i}'),
                    'desde': request.POST.get(f'MemberSince{i}'),
                    'hasta': request.POST.get(f'MemberUntil{i}'),
                    'is_current': False
                })
                i += 1

            # Procesar álbumes dinámicos
            i = 1
            while f'albumName{i}' in request.POST:
                data['albumes'].append({
                    'titulo': request.POST.get(f'albumName{i}'),
                    'año': request.POST.get(f'albumYear{i}'),
                    'duration_seconds': request.POST.get(f'albumDuration{i}'),
                    'cover_image_path': request.FILES.get(f'albumImage{i}').name if request.FILES.get(f'albumImage{i}') else None
                })
                i += 1

            # Procesar géneros y subgéneros (arrays)
            if 'generos[]' in request.POST:
                data['genre_ids'] = request.POST.getlist('generos[]')
            
            if 'subgeneros[]' in request.POST:
                data['subgenre_ids'] = request.POST.getlist('subgeneros[]')

            print("Datos a enviar a la API:", json.dumps(data, indent=2, ensure_ascii=False))
            print(data)
            # Enviar a la API externa
            #Enlace local http://127.0.0.1:5000
            response = requests.post(
                "http://127.0.0.1:5000/api/crear_artista_completo",
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            response.raise_for_status()

            return render(request, ruta_template, {
                "success": True,
                "response": response.json()
            })

        except requests.exceptions.HTTPError as e:
            error_message = f"Error de la API: {str(e)}"
            if e.response.status_code == 409:
                error_message = "El artista ya existe en el sistema"
            
            return render(request, ruta_template, {
                "error": error_message,
                "response": e.response.json() if e.response else None
            })

        except Exception as e:
            return render(request, ruta_template, {
                "error": f"Error interno: {str(e)}",
                "response": None
            })

"""
@csrf_exempt
def registrar_artista(request):
    if request.method == 'GET':
        return render(request, "Artista/registrar_artista.html")
    
    elif request.method == 'POST':
        try:
            # Cargar los datos JSON recibidos
            data = json.loads(request.body)
            
            # 1. Imprimir los datos recibidos (para verificación)
            print("\n--- DATOS RECIBIDOS DEL FORMULARIO ---")
            print(data)
            print("\n--- FIN DE DATOS RECIBIDOS ---\n")
            
            # 2. Enviar a la API externa
            api_url = 'https://musictreeapi.azurewebsites.net/api/crear_artista_completo'
            response = requests.post(
                api_url,
                json=data,  # Esto envía el JSON directamente
                headers={
                    'Content-Type': 'application/json',
                    # Agrega aquí otros headers necesarios (ej. API key)
                },
                timeout=10  # Tiempo de espera en segundos
            )
            
            # Verificar si la API respondió correctamente
            response.raise_for_status()
            
            # Opcional: Imprimir la respuesta de la API
            api_response = response.json()
            print("Respuesta de la API externa:", api_response)
            
            return JsonResponse({
                'success': True,
                'message': 'Artista creado exitosamente',
                'api_response': api_response  # Puedes omitir esto si no lo necesitas
            })
            
        except requests.exceptions.RequestException as e:
            print(f"Error al enviar a la API: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': f'Error al comunicarse con la API externa: {str(e)}',
                'error_details': str(e.response.text) if hasattr(e, 'response') else None
            }, status=500)
            
        except Exception as e:
            print(f"Error interno: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': f'Error interno del servidor: {str(e)}'
            }, status=500)
"""



def ver_catalogo_artista(request):
    ruta_catalogo_artistas = "Artista/ver_catalogo_artista.html"
    return render(request, ruta_catalogo_artistas)

def get_genres(request):
    """Endpoint para obtener géneros desde el API externo"""
    try:
        response = requests.get(
            'https://musictreeapi.azurewebsites.net/api/get_genres',
            timeout=5
        )
        response.raise_for_status()
        
        # Transforma los datos
        genres = [{
            'id': item['genre_id'],
            'nombre': item['name']
        } for item in response.json()]
        
        return JsonResponse(genres, safe=False)
        
    except Exception as e:
        # Datos de respaldo
        backup_data = [
            {'id': 'G-105AD5A53709000000000000', 'nombre': 'Rock'},
            {'id': 'G-792432650DE6000000000000', 'nombre': 'Jazz'}
        ]
        return JsonResponse(backup_data, safe=False)

def get_subgenres(request):
    """Endpoint para obtener géneros desde el API externo"""
    try:
        response = requests.get(
            'https://musictreeapi.azurewebsites.net/api/get_subgenres',
            timeout=5
        )
        response.raise_for_status()
        
        # Transforma los datos
        genres = [{
            'id': item['genre_id'],
            'nombre': item['name']
        } for item in response.json()]
        
        return JsonResponse(genres, safe=False)
        
    except Exception as e:
        # Datos de respaldo
        backup_data = [
            {'id': 'G-105AD5A53709000000000000', 'nombre': 'Rock'},
            {'id': 'G-792432650DE6000000000000', 'nombre': 'Jazz'}
        ]
        return JsonResponse(backup_data, safe=False)


@csrf_exempt
def ver_artista(request):
    ruta_ver_artista = "Artista/ver_artista.html"
    
    if request.method == 'GET' and 'search' in request.GET:
        try:
            artist_name = request.GET.get('search', '').strip()
            
            # Validar que el nombre no esté vacío
            if not artist_name:
                return render(request, ruta_ver_artista, {
                    'search_performed': True,
                    'error': 'Por favor ingresa un nombre de artista para buscar'
                })
            
            # Datos de ejemplo para pruebas (solo si se ingresó un nombre)
            mock_artist = {
                'name': artist_name,
                'image': "https://via.placeholder.com/300x300",
                'genres': ["Rock", "Pop"],
                'members': ["Vocalista", "Guitarrista", "Baterista"],
                'albums': [
                    {'title': "Álbum 1", 'date': "2020-01-01", 'image': "https://via.placeholder.com/150x150"},
                    {'title': "Álbum 2", 'date': "2022-05-15", 'image': "https://via.placeholder.com/150x150"}
                ],
                'photos': [
                    "https://via.placeholder.com/200x200",
                    "https://via.placeholder.com/200x200",
                    "https://via.placeholder.com/200x200"
                ],
                'comments': [
                    {'user': 'Fan1', 'text': '¡Gran concierto el año pasado!'},
                    {'user': 'Fan2', 'text': 'Me encanta su nueva canción.'}
                ],
                'events': [
                    {'date': '2023-12-15', 'time': '20:00', 'location': 'Estadio Nacional'},
                    {'date': '2024-02-20', 'time': '19:30', 'location': 'Arena Movistar'}
                ]
            }
            
            return render(request, ruta_ver_artista, {
                'artist': mock_artist,
                'search_performed': True
            })
            
        except Exception as e:
            return render(request, ruta_ver_artista, {
                'error': f"Error al buscar artista: {str(e)}",
                'search_performed': True
            })
    
    return render(request, ruta_ver_artista, {'search_performed': False})