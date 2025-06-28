import traceback
from utils.database.database import db
from sqlalchemy import text

def add_album_db(artist_id, album_data, release_date):
    #Ejecutar función PostgreSQL con parámetros exactos
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

    return result
    