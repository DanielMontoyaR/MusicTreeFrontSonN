from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
import requests


ruta_local_api = "http://127.0.0.1:5000/api/"
ruta_online_api = "https://musictreeapi.azurewebsites.net/api/reg_fanatico"

route = [ruta_local_api,ruta_online_api]

@csrf_exempt
def registrar_fanatico(request):
    ruta_template = "Fanatico/registrar_fanatico.html"
    
    if request.method == "GET":
        return render(request, ruta_template)
    
    if request.method != "POST":
        return JsonResponse({
            'success': False,
            'error': 'Método no permitido'
        }, status=405)
    
    try:        
        # Construir el objeto JSON con los datos del formulario
        data = {
            "username": request.POST.get("username"),
            "password": request.POST.get("password"),
            "fullname": request.POST.get("fullname"),
            "country": request.POST.get("pais"),
            "avatar": int(request.POST.get("avatar")),
            "favorite_genres": request.POST.getlist("generos[]")  # Cambiado a "generos" sin []
        }
        
        # Imprimir el JSON que se enviará a la API
        print("\nDatos a enviar a la API:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # Realizar la petición a la API
        response = requests.post(
            route[1] + "reg_fanatico",
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        # Si el backend responde correctamente
        response.raise_for_status()
        response_data = response.json()
        
        return JsonResponse({
            'success': True,
            'message': 'Fanático registrado exitosamente',
            'api_response': response_data
        })
    
    except requests.exceptions.HTTPError as e:
        # Manejo de errores HTTP de la API
        error_message = f"Error de la API: {str(e)}"
        if e.response.status_code == 409:
            error_message = "El nombre de usuario ya existe"
        
        return JsonResponse({
            'success': False,
            'error': error_message
        }, status=e.response.status_code)
    
    except Exception as e:
        # Manejo de otros errores
        print(f"Error interno al registrar fanático: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': f"Error interno: {str(e)}"
        }, status=500)