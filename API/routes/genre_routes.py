from flask import Blueprint, request, jsonify
from utils.queries.Genre.crear_genero import *
from utils.queries.Genre.get_generos import *
from utils.queries.Genre.get_subgeneros import *
from utils.queries.Genre.importjsongenre import *

genre_bp = Blueprint('genre_bp', __name__)

@genre_bp.route('/api/create_genres', methods=['POST'])
def crear_genero():
    data = request.get_json()
    try:
        genero, error_response, status_code = crearGeneroData(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return guardarGeneroDB(genero)

@genre_bp.route('/api/procesar-generos', methods=['POST'])
def procesar_generos():
    data = request.get_json()
    try:
        resultado, error_response, status_code = procesar_generos_batch(data)
        if error_response:
            return error_response, status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(resultado), status_code

@genre_bp.route('/api/get_genres', methods=['GET'])
def obtener_generos():
    return getGeneros()

@genre_bp.route('/api/get_subgenres', methods=['GET'])
def obtener_subgeneros():
    return getSubGeneros()
