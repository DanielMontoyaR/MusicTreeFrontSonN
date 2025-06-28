
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from flask import Flask, jsonify, render_template
from flask_cors import CORS  # Importa el módulo CORS
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

        #print(data)
        response = requests.post(
            route[0]+"crear_artista_completo",
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        # Añade manejo explícito de códigos de error
        if response.status_code >= 400:
            return JsonResponse({
                'success': False,
                'error': response.json().get('error', 'Error en la API'),
                'api_response': response.json()
            }, status=response.status_code)
            
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
            route[0]+"artists_view",
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
            route[0]+"get_genres",
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
            route[0]+"get_subgenres",
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
    
    if request.method == 'GET' and 'artist_id' in request.GET:
        try:
            artist_id = request.GET.get('artist_id')
            
            # Datos mock para pruebas - reemplazar con llamada a API real
            mock_artist = {
                "artist": {
                    "artist_id": artist_id,
                    "name": "Radiohead",
                    "biography": "Radiohead are an English rock band formed in Abingdon, Oxfordshire, in 1985. Known for their experimental approach to rock music.",
                    "country_of_origin": "Reino Unido",
                    "created_at": "2025-06-05T03:28:10.995408",
                    "cover_image_path": "https://cdn.discordapp.com/attachments/329398607021342721/1380021075643203584/Radioheadthebends.png",
                    "average_rating": 4.5,
                    "rating_count": 1250,
                    "activity_years": [
                        {"start_year": 1985, "end_year": None, "is_present": True}
                    ],
                    "genres": [
                        {"genre_id": "G-AA61F7B9765E000000000000", "name": "Rock"},
                        {"genre_id": "G-421E37BE0FA2000000000000", "name": "Alternative"}
                    ],
                    "subgenres": [
                        {"subgenre_id": "G-8D8E111CED4A000000000000", "name": "Alternative Rock"},
                        {"subgenre_id": "G-F17980CDAEE7000000000000", "name": "Experimental"}
                    ],
                    "members": [
                        {
                            "full_name": "Thom Yorke",
                            "instrument": "Voz, Guitarra, Piano",
                            "start_period": "1985",
                            "end_period": None,
                            "is_current": True
                        },
                        {
                            "full_name": "Jonny Greenwood",
                            "instrument": "Guitarra principal, Teclados",
                            "start_period": "1985",
                            "end_period": None,
                            "is_current": True
                        },
                        {
                            "full_name": "Colin Greenwood",
                            "instrument": "Bajo, Sintetizadores",
                            "start_period": "1985",
                            "end_period": None,
                            "is_current": True
                        },
                        {
                            "full_name": "Ed O'Brien",
                            "instrument": "Guitarra rítmica, Coros",
                            "start_period": "1985",
                            "end_period": None,
                            "is_current": True
                        },
                        {
                            "full_name": "Philip Selway",
                            "instrument": "Batería, Percusión",
                            "start_period": "1985",
                            "end_period": None,
                            "is_current": True
                        }
                    ],
                    "albums": [
                        {
                            "album_id": "A-5f2d0b6d290f-D-5a14e3661917",
                            "title": "Pablo Honey",
                            "release_date": "1993-02-22",
                            "cover_image_path": "https://upload.wikimedia.org/wikipedia/en/4/4d/Radiohead.pablohoney.albumart.jpg",
                            "duration_seconds": 2678
                        },
                        {
                            "album_id": "A-5f2d0b6d290f-D-6ec4d1c1b7ea",
                            "title": "The Bends",
                            "release_date": "1995-03-13",
                            "cover_image_path": "https://upload.wikimedia.org/wikipedia/en/4/4f/Radiohead.thebends.albumart.jpg",
                            "duration_seconds": 2923
                        },
                        {
                            "album_id": "A-5f2d0b6d290f-D-9f58eca93938",
                            "title": "OK Computer",
                            "release_date": "1997-05-21",
                            "cover_image_path": "https://upload.wikimedia.org/wikipedia/en/a/a1/Radiohead.okcomputer.albumart.jpg",
                            "duration_seconds": 5378
                        }
                    ],
                    "photos": [
                        {
                            "photo_id": 1,
                            "image_path": "https://upload.wikimedia.org/wikipedia/commons/7/7e/Radiohead_Oxford_2003.jpg",
                            "description": "Radiohead en concierto (2003)",
                            "upload_date": "2025-06-05T03:28:10.995408"
                        },
                        {
                            "photo_id": 2,
                            "image_path": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Radiohead_-_Glastonbury_2017_-_Sunday_-_JP_%2836697151054%29.jpg",
                            "description": "Presentación en Glastonbury 2017",
                            "upload_date": "2025-06-05T03:28:10.995408"
                        }
                    ],
                    "comments": [
                        {
                            "user": "Fan123",
                            "message": "¡La mejor banda de todos los tiempos!",
                            "date": "2025-01-15"
                        },
                        {
                            "user": "MusicLover",
                            "message": "Su evolución musical es increíble",
                            "date": "2025-02-20"
                        }
                    ],
                    "events": [
                        {
                            "date": "2023-12-15",
                            "time": "20:00",
                            "location": "Estadio Nacional, Santiago",
                            "description": "Tour 2023 - Presentando nuevo material"
                        }
                    ]
                }
            }
            
            # Transformar los datos para la plantilla
            transformed_artist = {
                'name': mock_artist['artist']['name'],
                'image': mock_artist['artist']['cover_image_path'],
                'biography': mock_artist['artist']['biography'],
                'country': mock_artist['artist']['country_of_origin'],
                'rating': mock_artist['artist']['average_rating'],
                'rating_count': mock_artist['artist']['rating_count'],
                'activity_periods': mock_artist['artist']['activity_years'],
                'genres': [g['name'] for g in mock_artist['artist']['genres']],
                'members': mock_artist['artist']['members'],
                'albums': mock_artist['artist']['albums'],
                'photos': mock_artist['artist']['photos'],
                'comments': mock_artist['artist']['comments'],
                'events': mock_artist['artist']['events']
            }
            
            return render(request, ruta_ver_artista, {
                'artist': transformed_artist
            })
            
        except Exception as e:
            return render(request, ruta_ver_artista, {
                'error': f"Error al cargar artista: {str(e)}"
            })
    
    return render(request, ruta_ver_artista)



@csrf_exempt
def buscar_artista_por_genero(request):
    ruta_buscar_artista_genero = "Artista/buscar_artista_genero.html"

    if request.method == "GET":
        return render(request, ruta_buscar_artista_genero)
    
    elif request.method != "POST":
        return JsonResponse({
            'success': False,
            'error': 'Método no permitido'
        }, status=405)
    
    try:
        data = json.loads(request.body)
        nombre = data.get('nombre', '').strip()
        genre_id = data.get('genre_id')
        subgenre_id = data.get('subgenre_id', [])
        limite = data.get('limite', 50)
        #print("Datos a enviar", data)
        # Validación básica
        if not genre_id:
            return JsonResponse({
                'success': False,
                'error': 'Se requiere un género principal'
            }, status=400)
        
        # Preparar datos para la API
        api_data = {
            "genre_id": genre_id,
            "subgenre_id": ",".join(subgenre_id) if subgenre_id else "",
            "nombre": nombre,
            "limite": limite
        }
        
        # Llamar a la API real
        response = requests.post(
            route[0] + "filtrar_artistas",
            json=api_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        response.raise_for_status()
        artists = response.json()
        print("ARTISTAS ENCONTRADOS", artists)
        return JsonResponse({
            'success': True,
            'artists': artists
        })
        
    except requests.exceptions.HTTPError as e:
        error_message = f"Error en la API: {str(e)}"
        if e.response.status_code == 404:
            error_message = "No se encontraron artistas con los criterios especificados"
        return JsonResponse({
            'success': False,
            'error': error_message
        }, status=e.response.status_code)
        
    except Exception as e:
        print(f"Error en búsqueda de artistas: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Error interno al realizar la búsqueda'
        }, status=500)