import traceback
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from utils.database.database import db
from sqlalchemy import text



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

        # Ejecutar función PostgreSQL con parámetros exactos
        query = text("""
            SELECT add_album(
                :p_artist_id,
                :p_title,
                CAST(:p_release_date AS DATE),
                :p_cover_image_path,
                :p_duration_seconds
            )
        """)

        result = db.session.execute(query, {
            'p_artist_id': artist_id,
            'p_title': album_data['titulo'],
            'p_release_date': release_date,
            'p_cover_image_path': album_data.get('cover_image_path'),
            'p_duration_seconds': album_data.get('duration_seconds', 0)
        })

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