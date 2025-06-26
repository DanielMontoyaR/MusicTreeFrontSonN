import traceback
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from utils.database.database import db
from utils.database.Artist.add_album_db import add_album_db



def guardar_album_individual(album_data, artist_id):
    """Función interna para guardar un solo álbum"""
    try:
        # Validaciones básicas
        if not artist_id:
            return None, jsonify({"error": "Artist ID inválido"}), 400

        if not album_data.get('titulo'):
            return None, jsonify({"error": "El título del álbum es obligatorio"}), 400

        # Procesar fecha (convertir año a fecha completa)
        release_year = album_data.get('año')
        try:
            release_date = f"{int(release_year)}-01-01" if release_year else None
        except ValueError:
            return None, jsonify({"error": "Año de lanzamiento inválido"}), 400
        
        result = add_album_db(artist_id, album_data, release_date)

        album_id = result.scalar()
        return album_id, None

    except IntegrityError as e:
        db.session.rollback()
        return None, jsonify({
            "error": "Error de integridad al guardar el álbum",
            "detalle": str(e.orig) if hasattr(e, 'orig') else str(e)
        }), 409

    except Exception as e:
        db.session.rollback()
        return None, jsonify({
            "error": "Error inesperado al guardar el álbum",
            "detalle": str(e),
            "trace": traceback.format_exc()
        }), 500

def guardar_albumes(data, artist_id):
    """
    Maneja el array completo de álbumes
    Args:
        albumes_data (list): Lista de diccionarios con datos de álbumes
        artist_id (str): ID del artista padre
    Returns:
        tuple: (lista de IDs, None) si éxito, (None, error_response) si falla
    """

    albumes_data = data.get('albumes', [])
    if not albumes_data:
        return [], None  # Caso sin álbumes

    album_ids = []
    for album in albumes_data:
        album_id, error = guardar_album_individual(album, artist_id)
        if error:
            return None, error
        album_ids.append(album_id)

    db.session.commit()
    return album_ids, None