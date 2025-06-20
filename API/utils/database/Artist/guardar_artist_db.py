import traceback
from utils.database.database import db
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from utils.models.artist_models import *
from sqlalchemy import func, text
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, BOOLEAN
from sqlalchemy import Numeric as DECIMAL

def guardarArtistaDB(artista):
    try:
        if artista is None:
            raise ValueError("No se pudo crear el objeto 'artista'. Verifique los datos de entrada.")

        query = text("""
            SELECT register_artist(
                :p_name,
                :p_biography,
                :p_country,
                :p_cover_image_path,
                :p_date_start,
                :p_date_end,
                :p_is_present,
                :p_genre_ids,
                :p_subgenre_ids
            )
        """)

        result = db.session.execute(query, {
            'p_name': artista['name'],
            'p_biography': artista['biography'],
            'p_country': artista['country'],
            'p_cover_image_path': artista['cover_image_path'],
            'p_date_start': artista['start_year'],
            'p_date_end': artista['end_year'],
            'p_is_present': artista['is_present'],
            'p_genre_ids': artista['genre_ids'],
            'p_subgenre_ids': artista['subgenre_ids']
        })

        artist_id = result.scalar()
        db.session.commit()

        # Devuelve None para error_response y el artist_id
        return None, artist_id

    except IntegrityError as e:
        db.session.rollback()
        error_response = jsonify({
            "error": "Restricción de integridad violada",
            "detalle": str(e)
        })
        return error_response, None

    except Exception as e:
        db.session.rollback()
        print("Error en servidor:", traceback.format_exc())
        error_response = jsonify({
            "error": "Error inesperado al registrar el artista",
            "detalle": str(e)
        })
        return error_response, None