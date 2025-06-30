# utils/controllers/artista/perfil_artista.py

import traceback
from flask import jsonify
from sqlalchemy import text
from utils.database.database import db
from utils.database.Artist.select_complete_artist import *

def obtenerPerfilArtista(data):
    try:
        artist_id = data.get('artist_id')

        if not artist_id:
            return None, jsonify({"error": "El campo 'artist_id' es obligatorio"}), 400
        
        result = obtenerPerfilArtistaCompleto(artist_id)
        row = result.fetchone()

        if not row:
            return None, jsonify({"error": "Artista no encontrado"}), 404

        return dict(row._mapping), None, None

    except Exception as e:
        db.session.rollback()
        return None, jsonify({
            "error": "Error interno al obtener el perfil del artista",
            "detalle": str(e),
            "trace": traceback.format_exc()
        }), 500
