
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from flask import Flask, jsonify, render_template
#from flask_cors import CORS  # Importa el módulo CORS
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests



import json
import re
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


ruta_local_api = "http://127.0.0.1:5000/api/"
ruta_online_api = "https://musictreeapi.azurewebsites.net/api/"

route = [ruta_local_api, ruta_online_api]



@csrf_exempt
def registrar_artista(request):
    ruta_template = "Artista/registrar_artista.html"

    if request.method == "GET":
        return render(request, ruta_template)

    if request.method != "POST":
        # Por si acaso llega otro verbo HTTP
        return render(request, ruta_template, {"error": "Método no permitido"}, status=405)

    try:
        data = {
            "is_band": request.POST.get("es_banda", "false") == "true",
            "nombre": request.POST.get("nombre"),
            "biografia": request.POST.get("biografia"),
            "pais": request.POST.get("pais"),
            "año_desde": request.POST.get("anio_desde"),
            "año_hasta": request.POST.get("anio_hasta"),
            "cover_image_path": (
                request.FILES.get("portada").name if request.FILES.get("portada") else None
            ),
            "miembros": [],
            "albumes": [],
            "genre_ids": [],
            "subgenre_ids": [],
        }

        # miembros dinámicos
        i = 1
        while f"MemberName{i}" in request.POST:
            data["miembros"].append(
                {
                    "nombre": request.POST.get(f"MemberName{i}"),
                    "instrumento": request.POST.get(f"MemberInstrument{i}"),
                    "desde": request.POST.get(f"MemberSince{i}"),
                    "hasta": request.POST.get(f"MemberUntil{i}"),
                    "is_current": False,
                }
            )
            i += 1

        # álbumes dinámicos
        i = 1
        while f"albumName{i}" in request.POST:
            data["albumes"].append(
                {
                    "titulo": request.POST.get(f"albumName{i}"),
                    "año": request.POST.get(f"albumYear{i}"),
                    "duration_seconds": request.POST.get(f"albumDuration{i}"),
                    "cover_image_path": (
                        request.FILES.get(f"albumImage{i}").name
                        if request.FILES.get(f"albumImage{i}")
                        else None
                    ),
                }
            )
            i += 1

        # géneros y subgéneros
        if "generos[]" in request.POST:
            data["genre_ids"] = request.POST.getlist("generos[]")
        if "subgeneros[]" in request.POST:
            data["subgenre_ids"] = request.POST.getlist("subgeneros[]")

        response = requests.post(
            route[1]+"crear_artista_completo",
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        # Si el backend responde 2xx, todo bien:
        response.raise_for_status()
        return JsonResponse({
            'success': True,
            'message': 'Artista registrado exitosamente'
        })

    except requests.exceptions.HTTPError as e:
        # Mantén tu lógica original de manejo de errores
        detalle = ""
        try:
            err_json = e.response.json()
            detalle = err_json.get("detalle", "")
        except Exception:
            err_json = None

        if "psycopg2.errors.UniqueViolation" in detalle:
            match = re.search(r"Key \(name\)=\((.*?)\)", detalle)
            artista_dup = match.group(1) if match else "el artista"
            error_message = f"Error: el nombre del artista «{artista_dup}» ya existe en el sistema"
        elif e.response.status_code == 409:
            error_message = "El artista ya existe en el sistema"
        else:
            error_message = f"Error de la API: {str(e)}"

        return JsonResponse({
            'success': False,
            'error': error_message
        }, status=e.response.status_code)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f"Error interno: {str(e)}"
        }, status=500)

def ver_catalogo_artista(request):
    ruta_catalogo_artistas = "Artista/ver_catalogo_artista.html"
    
    try:
        # Obtener datos de la API
        response = requests.get(
            route[1]+"artists_view",
            timeout=5
        )
        
        response.raise_for_status()
        
        # Transformar los datos a la estructura que espera la plantilla
        artistas = []
        for artista in response.json():
            artistas.append({
                'id': artista.get('ID Artista', ''),
                'nombre': artista.get('Nombre', ''),
                'pais': artista.get('País de Origen', ''),
                'albums_count': artista.get('Álbumes Asociados', 0),
                'fecha_creacion': artista.get('Fecha y Hora de Registro', ''),
                'años_actividad': artista.get('Años de Actividad', ''),
                'estado': artista.get('Estado', '')
            })
        
        # Ordenar por fecha de registro (más recientes primero)
        artistas.sort(key=lambda x: x['fecha_creacion'], reverse=True)
        
        return render(request, ruta_catalogo_artistas, {
            'artistas': artistas
        })
        
    except requests.exceptions.RequestException as e:
        # En caso de error, mostrar catálogo vacío con mensaje
        print(f"Error al obtener artistas: {str(e)}")
        return render(request, ruta_catalogo_artistas, {
            'artistas': [],
            'error': 'No se pudo cargar el catálogo de artistas. Por favor intenta más tarde.'
        })

def get_genres(request):
    """Endpoint para obtener géneros desde el API externo"""
    try:
        response = requests.get(
            route[1]+"get_genres",
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
            route[1]+"get_subgenres",
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



@csrf_exempt
def buscar_artista_por_genero(request):
    ruta_buscar_artista_genero = "Artista/buscar_artista_genero.html"

    if request.method=="GET":
        return render(request, ruta_buscar_artista_genero)
    
    elif request.method != "POST":
        return JsonResponse({
            'success': False,
            'error': 'Método no permitido'
        }, status=405)
    
    try:
        data = json.loads(request.body)
        artist_name = data.get('artist_name', '').strip().lower()
        main_genre = data.get('main_genre').strip().lower() #'Rock'
        subgenres = data.get('subgenres', [])
        

        print("El usuario busca a alguien con el género", main_genre)
        # Validación básica
        if not main_genre:
            return JsonResponse({
                'success': False,
                'error': 'Se requiere un género principal'
            }, status=400)
        
        # Simulación de datos para pruebas
        mock_artists = [
            {
                'id': 'A1',
                'name': 'Artista de Rock 1',
                'image': 'https://via.placeholder.com/150',
                'albums_count': 5,
                'genres': ['g-421e37be0fa2000000000000'],
                'subgenres': ['Rock Alternativo']
            },
            {
                'id': 'A2',
                'name': 'Artista de Pop 1',
                'image': 'https://via.placeholder.com/150',
                'albums_count': 3,
                'genres': ['g-421e37be0fa2000000000000'],
                'subgenres': ['Pop Rock']
            },
            {
                'id': 'A3',
                'name': 'Artista Mixto',
                'image': 'https://via.placeholder.com/150',
                'albums_count': 7,
                'genres': ['Rock', 'Pop'],
                'subgenres': ['Rock Clásico', 'Pop Electrónico']
            }
        ]
        
        # Filtrar por género principal (convertimos todo a minúsculas para comparar)
        filtered_artists = [
            artist for artist in mock_artists
            if main_genre in [g.lower() for g in artist['genres']]
        ]
        print(f"Artistas después de filtrar por género principal ({main_genre}): {len(filtered_artists)}")

        # Filtrar por subgéneros si se especificaron
        if subgenres:
            filtered_artists = [
                artist for artist in filtered_artists
                if any(
                    any(sg in s.lower() for s in artist.get('subgenres', []))
                    for sg in subgenres
                )
            ]
            print(f"Artistas después de filtrar por subgéneros: {len(filtered_artists)}")
        
        # Filtrar por nombre de artista si se especificó
        if artist_name:
            filtered_artists = [
                artist for artist in filtered_artists
                if artist_name in artist['name'].lower()
            ]
            print(f"Artistas después de filtrar por nombre: {len(filtered_artists)}")
        
        return JsonResponse({
            'success': True,
            'artists': filtered_artists
        })
        
    except Exception as e:
        print(f"Error en búsqueda de artistas: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Error interno al realizar la búsqueda'
        }, status=500)
