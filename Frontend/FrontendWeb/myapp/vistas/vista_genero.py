from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from flask import Flask, jsonify, render_template
#from flask_cors import CORS  # Importa el módulo CORS
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import ClusterGenero  # Asegúrate de importar tu modelo
import json
import requests

@csrf_exempt
def crear_genero_musica(request):

    ruta_crear_genero = "Genero/crear_genero_musica.html"

    if request.method == 'POST':
        try:
            data = {
                'genre_id': request.POST.get('genre_id'),
                'name': request.POST.get('name'),
                'description': request.POST.get('description'),
                'is_active': request.POST.get('is_active', 'false') == 'true',
                'color': request.POST.get('color'),
                'creation_year': int(request.POST.get('creation_year')),
                'country_of_origin': request.POST.get('country_of_origin'),
                'average_mode': request.POST.get('average_mode'),
                'bpm_lower': request.POST.get('bpm_lower'),
                'bpm_upper': request.POST.get('bpm_upper'),
                'dominant_key': request.POST.get('dominant_key'),
                'typical_volume': request.POST.get('typical_volume'),
                'time_signature': request.POST.get('time_signature'),
                'average_duration': request.POST.get('average_duration'),
                'is_subgenre': request.POST.get('is_subgenre', 'false') == 'true',
                'parent_genre_id': request.POST.get('parent_genre_id'),
                'cluster_id': request.POST.get('cluster_id'),
            }

            print("Data to send:", data)  # Debugging

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
def importar_generos(request):

    ruta_importar_genero = "Genero/importar_generos.html"

    return render(request, ruta_importar_genero)