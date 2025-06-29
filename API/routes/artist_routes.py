from flask import Blueprint, request, jsonify
from sqlalchemy import text
from utils.database.database import db
from utils.queries.Artist.crear_artista import crearArtistaData
from utils.database.Artist.guardar_artist_db import guardarArtistaDB
from utils.database.Artist.rate_artist_db import ejecutar_rate_artist_DB
from utils.queries.Artist.guardar_album import *
from utils.queries.Artist.guardar_miembro import *
from utils.queries.Artist.get_artists import *
from utils.queries.Artist.rate_artist import *
from utils.logging.logger import configurar_logger

artist_bp = Blueprint('artist_bp', __name__)

@artist_bp.route('/api/crear_artista_completo', methods=['POST'])
def crear_artista_completo():
    data = request.get_json()
    try:
        artista_data, error_response, status_code = crearArtistaData(data)
        if error_response:
            return error_response, status_code

        error_response, artist_id = guardarArtistaDB(artista_data)
        if error_response:
            return error_response, 400

        album_ids, error_response = guardar_albumes(data, artist_id)
        if error_response:
            return error_response, 400

        error_response, status_code = guardarMiembro(data, artist_id)
        if error_response:
            return error_response, status_code

        return jsonify({
            "mensaje": "Artista, álbumes y miembros registrados exitosamente.",
            "artist_id": artist_id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@artist_bp.route('/api/artists_view')
def get_artist_view():
    return getArtists()

@artist_bp.route('/api/search_artist', methods=['POST'])
def buscar_artista():
    data = request.get_json()
    try:
        search_term = data.get('search')
        if not search_term:
            return jsonify({"error": "Falta el parámetro 'search'"}), 400

        result = db.session.execute(
            text("SELECT * FROM search_artist_json(:search_term)"),
            {"search_term": search_term}
        )
        artists = [dict(row._mapping) for row in result]
        return jsonify(artists)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@artist_bp.route("/api/rate_artist", methods=["POST"])
def rate_artist():
    data = request.get_json()
    try:
        error_resp, status_code, valid_data = validar_rate_artist(data)
        if error_resp:
            return error_resp, status_code

        return ejecutar_rate_artist_DB(valid_data)

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Error inesperado",
            "detalle": str(e)
        }), 500
