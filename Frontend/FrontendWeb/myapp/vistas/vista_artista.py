
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

    ruta_crear_artista = "Artista/registrar_artista.html"

    return render(request, ruta_crear_artista)

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