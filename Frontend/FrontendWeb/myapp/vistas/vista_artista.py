
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from flask import Flask, jsonify, render_template
from flask_cors import CORS  # Importa el módulo CORS
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests




@csrf_exempt
def registrar_artista(request):

    ruta_crear_artista = "Artista/registrar_artista.html"

    return render(request, ruta_crear_artista)