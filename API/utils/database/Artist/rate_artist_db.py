import uuid
from sqlalchemy import text
from utils.database.database import db

def ejecutar_rate_artist_DB(fan_id, artist_id, rating):
    sql = text("SELECT * FROM rate_artist(:fan_id, :artist_id, :rating)")
    result = db.session.execute(sql, {
        "fan_id": fan_id,
        "artist_id": artist_id,
        "rating": rating
    }).scalar()
    return result