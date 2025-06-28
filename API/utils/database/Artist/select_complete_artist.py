import traceback
from sqlalchemy import text
from utils.database.database import db

def obtenerPerfilArtistaCompleto(artist_id):

    query = text("SELECT * FROM get_artist_profile(:artist_id)")
    result = db.session.execute(query, {"artist_id": artist_id})
    
    return result