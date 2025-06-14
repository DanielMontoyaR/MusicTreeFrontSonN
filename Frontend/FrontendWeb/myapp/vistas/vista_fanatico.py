
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from flask import Flask, jsonify, render_template
#from flask_cors import CORS  # Importa el módulo CORS
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests


ruta_local_api = "http://127.0.0.1:5000/api/"
ruta_online_api = "https://musictreeapi.azurewebsites.net/"

def registrar_fanatico(request):
    ruta_home = "Fanatico/registrar_fanatico.html"
    return render(request, ruta_home)