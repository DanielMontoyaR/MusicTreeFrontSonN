from flask import Blueprint, request, jsonify
from utils.queries.Fanatico.login_fan import *
from utils.queries.Fanatico.crear_fanatico import *
from utils.database.Fanatico.guardar_fanatico_db import guardarFanaticoDB
from utils.queries.Fanatico.filtrar_artistas import *
from utils.database.database import db

fan_bp = Blueprint('fan_bp', __name__)

@fan_bp.route('/api/login_fan', methods=['POST'])    
def login_fan():
    data = request.get_json()
    try:
        result, error_response, status_code = loginFanData(data)
        if error_response:
            return error_response, status_code
        return jsonify(result), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@fan_bp.route('/api/registro_fanatico', methods=['POST'])
def crear_fanatico():
    data = request.get_json()
    try:
        fanaticoData, error_response, status_code = crearFanatico(data)
        if error_response:
            return error_response, status_code
        return guardarFanaticoDB(fanaticoData)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@fan_bp.route('/api/filtrar_artistas', methods=['POST'])
def filtrar_artistas():
    data = request.get_json()
    try:
        resultado, error_response, status_code = buscarArtistasFiltrados(data)
        if error_response:
            return error_response, status_code
        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({
            "error": "Error inesperado al procesar la solicitud",
            "detalle": str(e)
        }), 500
