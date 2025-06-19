from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
import requests


ruta_local_api = "http://127.0.0.1:5000/api/"
ruta_online_api = "https://musictreeapi.azurewebsites.net/api/"

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
            route[1] + "registro_fanatico",
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
    

@csrf_exempt
def login_fanatico(request):
    ruta_fanatico = "Fanatico/login_fanatico.html"
    if request.method == "GET":
        return render(request, ruta_fanatico)
    
    elif request.method != "POST":
        return JsonResponse({
            'success': False, 
            'error': 'Método no permitido'
        }, status=405)
    
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        # Validación mejorada
        if not username or not password:
            return JsonResponse({
                'success': False,
                'error': 'Usuario y contraseña son requeridos'
            }, status=400)
        
        # Debug seguro (no mostrar contraseña)
        print(f"\nIntento de login para usuario: {username} con contraseña {password} ")
        
        # Configurar timeout para la API
        api_timeout = 10  # segundos
        
        response = requests.post(
            f"{ruta_online_api}login_fanatico",
            json={
                'username': username,
                'password': password
            },
            headers={'Content-Type': 'application/json'},
            timeout=api_timeout
        )
        
        response.raise_for_status()
        api_data = response.json()
        
        return JsonResponse({
            'success': True,
            'message': 'Autenticación exitosa',
            'user_data': {  # Ejemplo de datos que podrías recibir
                'username': username,
                'token': api_data.get('token'),
                'avatar': api_data.get('avatar')
            }
        })
        
    except requests.exceptions.Timeout:
        print("Error: Tiempo de espera agotado al conectar con la API")
        return JsonResponse({
            'success': False,
            'error': 'El servidor no responde. Intente más tarde'
        }, status=504)
        
    except requests.exceptions.HTTPError as e:
        error_msg = "Credenciales inválidas"
        if e.response.status_code == 400:
            try:
                error_data = e.response.json()
                error_msg = error_data.get('detail', error_msg)
            except:
                pass
        return JsonResponse({
            'success': False,
            'error': error_msg
        }, status=e.response.status_code)
        
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Error interno del servidor'
        }, status=500)

def generos_musicales(request):
    try:
        # Obtener géneros de la API
        response = requests.get(
            route + "get_genres",
            timeout=5
        )
        response.raise_for_status()
        
        # Ordenar alfabéticamente
        generos = sorted(response.json(), key=lambda x: x['name'])
        
        return render(request, "Generos/lista_generos.html", {
            'generos': generos
        })
        
    except Exception as e:
        print(f"Error al obtener géneros: {str(e)}")
        # Datos de ejemplo en caso de error
        generos = [
            {'genre_id': 'G-1', 'name': 'Rock', 'description': 'Género popular', 'origin': 'Años 50'},
            {'genre_id': 'G-2', 'name': 'Pop', 'description': 'Música popular', 'origin': 'Años 60'}
        ]
        return render(request, "Generos/lista_generos.html", {
            'generos': generos,
            'error': 'No se pudieron cargar los géneros desde la API'
        })