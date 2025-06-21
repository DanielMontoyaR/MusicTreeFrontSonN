from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

ruta_local_api = "http://127.0.0.1:5000/api/"
ruta_online_api = "https://musictreeapi.azurewebsites.net/api/"

route = [ruta_local_api,ruta_online_api]  # Usamos la API online por defecto


def home(request):
    ruta_home = "Home/home.html"
    return render(request, ruta_home)

