from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

ruta_local_api = "http://127.0.0.1:5000/api/"
ruta_online_api = "https://musictreeapi.azurewebsites.net/"

route = [ruta_local_api, ruta_online_api]

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
                route[0]+"create_cluster_genero",
                json=data
            )
            response.raise_for_status()
            return render(request, ruta_crear_cluster, {
                "success": True, 
                "response": response.json()
            })
        
        except requests.exceptions.HTTPError as e:
            error_message = f"Error en la API: {str(e)}"
            if e.response.status_code == 500:
                error_message = "Error: El nombre ya existe en el sistema. No se puede crear un cluster duplicado."
            return render(request, ruta_crear_cluster, {
                "error": error_message,
                "response": e.response.json() if e.response else None
            })
            
        except Exception as e:
            return render(request, ruta_crear_cluster, {
                "error": f"Error inesperado: {str(e)}",
                "response": None
            })
        
    return render(request, ruta_crear_cluster)

def get_cluster_genero(request):
    ruta_get_cluster = "Cluster/get_cluster_genero.html"
    context = {
        "Clusters": [],
        "mostrar_inactivos": False,
        "error": None
    }
    
    if request.method == 'GET':
        try:
            response = requests.get(route[0]+"get_clusters_genero")
            response.raise_for_status()
            clusters = response.json()

            cluster_sorted = sorted(clusters, key=lambda x: x['name'].lower())
            mostrar_inactivos = request.GET.get('mostrar_inactivos', 'false') == 'true'
            if not mostrar_inactivos:
                cluster_sorted = [cluster for cluster in cluster_sorted if cluster['is_active']]
            
            context.update({
                "Clusters": cluster_sorted,
                "mostrar_inactivos": mostrar_inactivos
            })
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 500:
                context["error"] = "Error interno del servidor al obtener clusters"
            else:
                context["error"] = f"Error al obtener clusters: {e.response.text}"
            
        except Exception as e:
            context["error"] = f"Error inesperado al obtener clusters: {str(e)}"
    
    # Asegurarse de que siempre devolvemos el contexto
    return render(request, ruta_get_cluster, context)