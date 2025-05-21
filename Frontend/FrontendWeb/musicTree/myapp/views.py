from django.shortcuts import render, HttpResponse
from .models import TodoItem
from .models import ClusterGenero
# Create your views here.
from django.http import JsonResponse
from .models import ClusterGenero
from django.views.decorators.csrf import csrf_exempt
import json
from flask import Flask, jsonify, render_template
from flask_cors import CORS  # Importa el módulo CORS

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ClusterGenero  # Asegúrate de importar tu modelo
import json
import requests

def get_cluster_genero(request):
    if request.method == 'GET':
        try:
            response = requests.get("https://musictreeapi.azurewebsites.net/get_clusters_genero")
            response.raise_for_status()
            clusters = response.json()

            cluster_sorted = sorted(clusters, key=lambda x: x['name'].lower())
            #Filtrar inactivos
            mostrar_inactivos = request.GET.get('mostrar_inactivos', 'false') == 'true'
            if not mostrar_inactivos:
                cluster_sorted = [cluster for cluster in cluster_sorted if cluster['is_active']]
            print(clusters)  # Imprime la respuesta para depuración
            return render(request, "get_cluster_genero.html", {"Clusters": clusters, "mostrar_inactivos": mostrar_inactivos})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def home(request):
    #return HttpResponse("hello world!")
    return render(request, "home.html")

def todos(request):
    items = TodoItem.objects.all()
    return render(request, "todos.html",{"todos": items})

def main_menu(request):
    return render(request, "main_menu.html")

@csrf_exempt
def crear_cluster(request):
    if request.method == 'POST':
        try:
            data = {
                'cluster_id': request.POST.get('cluster_id'),
                'name': request.POST.get('name'),
                'description': request.POST.get('description'),
                'is_active': request.POST.get('is_active', 'false') == 'true'
            }

            print("Data to send:", data)  # Imprime los datos para depuración

            response = requests.post(
                "http://127.0.0.1:5000/create_cluster_genero",
                json=data
            )
            response.raise_for_status()
            return render(request, "crear_cluster.html", {"success": True, "response": response.json()})
        except Exception as e:
            return render(request, "crear_cluster.html", {"error": str(e)})
    return render(request, "crear_cluster.html")

#def crear_cluster(request):    
#    return render(request,"crear_cluster.html")

@csrf_exempt
def crear_genero_musica(request):
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
                "http://127.0.0.1:5000/api/create_genres",
                json=data
            )
            response.raise_for_status()
            return render(request, "crear_genero_musica.html", {"success": True, "response": response.json()})
        except Exception as e:
            return render(request, "crear_genero_musica.html", {"error": str(e)})
    return render(request, "crear_genero_musica.html")

#def crear_genero_musica(request):
#    return render(request, "crear_genero_musica.html")