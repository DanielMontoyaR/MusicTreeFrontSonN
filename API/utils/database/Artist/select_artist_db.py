from sqlalchemy import text
from utils.database.database import db

def selectArtistDataDB(genre_id, subgenre_id, nombre, limite):
      # Ejecutar función SQL
        query = text("""
            SELECT * FROM search_artists_by_genre(
                :p_genre_id,
                :p_subgenre_id,
                :p_name_filter,
                :p_limit
            )
        """)

        result = db.session.execute(query, {
            'p_genre_id': genre_id,
            'p_subgenre_id': subgenre_id,
            'p_name_filter': nombre,
            'p_limit': limite
        })

        return result 