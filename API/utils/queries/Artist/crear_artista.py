import traceback
from utils.database.database import db
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from utils.models.artist_models import *
from sqlalchemy import func, text
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, BOOLEAN
from sqlalchemy import Numeric as DECIMAL

def crearArtistaData(data):
    try:
        # Validaciones básicas obligatorias
        if not data.get('nombre') or len(data['nombre']) < 3:
            return None, jsonify({"error": "El nombre es obligatorio y debe tener al menos 3 caracteres"}), 400

        if not data.get('pais'):
            return None, jsonify({"error": "El país de origen es obligatorio"}), 400

        if not data.get('año_desde'):
            return None, jsonify({"error": "El año de inicio (año_desde) es obligatorio"}), 400

        # Procesar años y estado de actividad
        try:
            start_year = int(data['año_desde'])
        except ValueError:
            return None, jsonify({"error": "El año de inicio debe ser un número válido"}), 400

        end_year_raw = data.get('año_hasta', None) 

        if end_year_raw and isinstance(end_year_raw, str) and end_year_raw.strip().lower() == "presente":
            end_year = None
            is_present = True
        else:
            is_present = False
            try:
                end_year = int(end_year_raw) if end_year_raw else None
            except ValueError:
                return None, jsonify({"error": "El año de fin debe ser un número válido o 'presente'"}), 400

        # Géneros y subgéneros
        genre_ids = data.get('genre_ids', [])
        subgenre_ids = data.get('subgenre_ids', [])

        if not isinstance(genre_ids, list) or not all(isinstance(g, str) for g in genre_ids):
            return None, jsonify({"error": "genre_ids debe ser una lista de strings"}), 400

        if not isinstance(subgenre_ids, list) or not all(isinstance(s, str) for s in subgenre_ids):
            return None, jsonify({"error": "subgenre_ids debe ser una lista de strings"}), 400

        # Datos opcionales
        biography = data.get('biografia', '')
        cover_image_path = data.get('cover_image_path', None)

        artista = {
            "name": data['nombre'],
            "biography": biography,
            "country": data['pais'],
            "cover_image_path": cover_image_path,
            "start_year": start_year,
            "end_year": end_year,
            "is_present": is_present,
            "genre_ids": genre_ids,
            "subgenre_ids": subgenre_ids
        }

        return artista, None, None

    except Exception as e:
        return None, jsonify({
            "error": "Error procesando datos del artista",
            "detalle": str(e),
            "trace": traceback.format_exc()
        }), 500

