import traceback
from utils.database.database import db
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from utils.models.genre_models import Genre
from sqlalchemy import func, text
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, BOOLEAN
from sqlalchemy import Numeric as DECIMAL


def safe_float(value):
    return float(value) if value is not None else None

def guardarGeneroDB(genero):
    try:
        if genero is None:
            raise ValueError("Failed to create 'genero' object. Check input data.")

        query = text("""
            SELECT create_genre(
                :name, :description, :color, :creation_year, :country,
                :average_mode, :bpm_lower, :bpm_upper, :dominant_key, :volume,
                :time_signature, :duration, :is_subgenre, :parent_genre_id, :cluster_id
            )
        """)

        # Execute with type hints in the parameters dictionary
        result = db.session.execute(
            query,
            {
                'name': genero.name,
                'description': genero.description,
                'color': None if genero.is_subgenre else genero.color,
                'creation_year': genero.creation_year,
                'country': genero.country_of_origin,
                'average_mode': safe_float(genero.average_mode),
                'bpm_lower': genero.bpm_lower,
                'bpm_upper': genero.bpm_upper,
                'dominant_key': str(genero.dominant_key),
                'volume': safe_float(genero.typical_volume),
                'time_signature': str(genero.time_signature),
                'duration': genero.average_duration,
                'is_subgenre': genero.is_subgenre,
                'parent_genre_id': genero.parent_genre_id,
                'cluster_id': genero.cluster_id
            }
        )

        genre_id = result.scalar()
        print("Género creado con ID:", genre_id)  # Log para verificar el ID generado
        db.session.commit()

        return jsonify({
            "mensaje": "Género creado exitosamente",
            "genre_id": genero.genre_id
        }), 201

    except IntegrityError as e:
        db.session.rollback()
        if 'unique constraint' in str(e.orig):
            return jsonify({"error": f"El género '{genero.name}' ya existe"}), 409
        return jsonify({"error": "Error de integridad", "detalle": str(e)}), 400
    
    except Exception as e:
       db.session.rollback()
       print("Error en servidor:", traceback.format_exc())  # Log detallado en consola
       return jsonify({
            "error": "Error inesperado",
            "detalle": str(e)
        }), 500 