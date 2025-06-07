from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from flask import Flask, jsonify, render_template
from flask_cors import CORS  # Importa el módulo CORS
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import ClusterGenero  # Asegúrate de importar tu modelo
import json
import requests
import logging

@csrf_exempt
def crear_genero_musica(request):

    ruta_crear_genero = "Genero/crear_genero_musica.html"

    if request.method == 'POST':
        try:
            data = {
                'name': request.POST.get('name'),
                'description': request.POST.get('description'),
                'color': request.POST.get('color'),
                'creation_year': int(request.POST.get('creation_year')),
                'country_of_origin': request.POST.get('country_of_origin'),
                'average_mode': float(request.POST.get('average_mode')),
                'bpm_lower': int(request.POST.get('bpm_lower')),
                'bpm_upper': int(request.POST.get('bpm_upper')),
                'dominant_key': request.POST.get('dominant_key'),
                'typical_volume': float(request.POST.get('typical_volume')),
                'time_signature': request.POST.get('time_signature'),
                'average_duration': int(request.POST.get('average_duration')),
                'is_subgenre': request.POST.get('is_subgenre') == 'on',
                'parent_genre_id': request.POST.get('parent_genre_id'),
                'cluster_id': request.POST.get('cluster_id'),

                #'genre_id': request.POST.get('genre_id'),
                #'is_active': request.POST.get('is_active', 'false') == 'true',
            }
            print("Data to send:", data)  # Debugging
            #Link local http://127.0.0.1:5000
            response = requests.post(
                "https://musictreeapi.azurewebsites.net/api/create_genres",
                json=data
            )
            response.raise_for_status()
            return render(request, ruta_crear_genero, {"success": True, "response": response.json()})
        except Exception as e:
            return render(request, ruta_crear_genero, {"error": str(e)})
    return render(request, ruta_crear_genero)

@csrf_exempt
def get_clusters(request):
    """Endpoint para obtener clusters desde el API externo"""
    try:
        response = requests.get(
            'https://musictreeapi.azurewebsites.net/api/get_clusters',
            timeout=5  # 5 segundos de timeout
        )
        response.raise_for_status()  # Lanza error si hay problemas
        
        # Transforma los datos para mantener consistencia
        clusters = [{
            'id': item['cluster_id'],
            'nombre': item['name']
        } for item in response.json()]
        
        return JsonResponse(clusters, safe=False)
        
    except Exception as e:
        # Retorna datos mockeados si falla la conexión (para desarrollo)
        backup_data = [
            {'id': 'C-D067F8195E78', 'nombre': 'Popular Music'},
            {'id': 'C-EFB0A68EAEA5', 'nombre': 'Traditional'}
        ]
        return JsonResponse(backup_data, safe=False)



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


logger = logging.getLogger(__name__)          # usa logging en lugar de print

@csrf_exempt
def importar_generos(request):
    template = "Genero/importar_generos.html"

    if request.method != "POST":
        return render(request, template)

    try:
        data = json.loads(request.body)

        # Llamada a la API externa
        api_resp = requests.post(
            "https://musictreeapi.azurewebsites.net/api/procesar-generos",
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=30,
        )

        try:
            api_json = api_resp.json()
        except ValueError:
            return JsonResponse(
                {
                    "success": False,
                    "error": "La API no devolvió JSON válido",
                },
                status=502,
            )

        errores = api_json.get("errores", [])
        if errores:
            mensajes_errores = []
            status_code = 400  # valor por defecto si no hay 500

            for error in errores:
                codigo = error.get("status_code", 400)
                index = error.get("index", -1)

                if codigo == 500:
                    mensajes_errores.append(
                        f"Error: se está intentando ingresar un género repetido en la posición {index}"
                    )
                    status_code = 500 
                else:
                    mensajes_errores.append(
                        f"Error en posición {index}: {error.get('error', 'Error desconocido')}"
                    )
            print("ERROR: " ,mensajes_errores)
            return JsonResponse(
                {
                    "success": False,
                    "status_code": status_code,
                    "errores": mensajes_errores,
                    "mensaje": api_json.get("mensaje", ""),
                },
                status=status_code,
            )

        return JsonResponse(
            {
                "success": True,
                "data": api_json,
            }
        )
    

    except requests.exceptions.RequestException as e:
        return JsonResponse(
            {"success": False, "error": f"Error al conectar con la API: {e}"},
            status=502,
        )
    except Exception as e:
        return JsonResponse(
            {"success": False, "error": f"Error interno: {e}"},
            status=500,
        )
    
