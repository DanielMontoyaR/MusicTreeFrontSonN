import traceback
from utils.database.database import db
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from utils.models.artist_models import *
from sqlalchemy import func, text
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, BOOLEAN
from sqlalchemy import Numeric as DECIMAL

import traceback
from flask import jsonify

def crearFanatico(data):
    try:
        # Validaciones obligatorias
        if not data.get('username') or len(data['username']) < 3:
            return None, jsonify({"error": "El nombre de usuario es obligatorio y debe tener al menos 3 caracteres"}), 400

        if not data.get('password') or len(data['password']) < 8:
            return None, jsonify({"error": "La contraseña debe tener al menos 8 caracteres"}), 400

        if not data.get('fullname') or len(data['fullname']) < 3:
            return None, jsonify({"error": "El nombre completo es obligatorio"}), 400

        if not data.get('country'):
            return None, jsonify({"error": "El país es obligatorio"}), 400

        if not data.get('avatar'):
            return None, jsonify({"error": "El avatar es obligatorio"}), 400

        # Validar que el avatar sea un número válido (1-9)
        try:
            avatar_id = int(data['avatar'])
            if avatar_id < 1 or avatar_id > 9:
                return None, jsonify({"error": "El avatar debe estar entre 1 y 9"}), 400
        except ValueError:
            return None, jsonify({"error": "El avatar debe ser un número entero"}), 400

        # Validar géneros favoritos
        favorite_genres = data.get('favorite_genres', [])
        if not isinstance(favorite_genres, list) or not all(isinstance(g, str) for g in favorite_genres):
            return None, jsonify({"error": "favorite_genres debe ser una lista de strings"}), 400

        if len(favorite_genres) == 0:
            return None, jsonify({"error": "Debe seleccionar al menos un género favorito"}), 400

        fanatico = {
            "username": data['username'],
            "password": data['password'],  # Aquí aún en texto plano, se puede hashear después si deseas
            "fullname": data['fullname'],
            "country": data['country'],
            "avatar": avatar_id,
            "favorite_genres": favorite_genres
        }

        return fanatico, None, None

    except Exception as e:
        return None, jsonify({
            "error": "Error procesando datos del fanático",
            "detalle": str(e),
            "trace": traceback.format_exc()
        }), 500

