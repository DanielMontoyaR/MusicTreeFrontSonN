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



@csrf_exempt
def crear_cluster(request):
    ruta_crear_cluster = "Cluster/crear_cluster.html"
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
                "https://musictreeapi.azurewebsites.net/create_cluster_genero",
                json=data
            )
            response.raise_for_status()
            return render(request, ruta_crear_cluster, {"success": True, "response": response.json()})
        except Exception as e:
            return render(request, ruta_crear_cluster, {"error": str(e)})
    return render(request, ruta_crear_cluster)

def get_cluster_genero(request):
    ruta_get_cluster = "Cluster/get_cluster_genero.html"
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
            return render(request, ruta_get_cluster, {"Clusters": clusters, "mostrar_inactivos": mostrar_inactivos})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


