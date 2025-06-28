import uuid
from utils.database.database import db

def ejecutarBusquedaDB(text):
         
    query = text("""
        SELECT search_artist_json(
            :p_search_term
        )
    """)

    # Execute with type hints in the parameters dictionary
    result = db.session.execute(
        query,
        {
            'p_search_term': text.name,
        }
    )

    return result 
