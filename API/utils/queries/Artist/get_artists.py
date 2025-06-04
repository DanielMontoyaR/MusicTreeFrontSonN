from flask import jsonify
from sqlalchemy.exc import IntegrityError
# Assuming you have an Artist model defined in your models.py
from utils.models.models import Artist

def getArtists():
    try:
        
        artists = Artist.query.filter_by(is_active=True).all()
        artists_json = [artist.partial_to_dict() for artist in artists]
        
        return jsonify(artists_json), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener los artistas: {str(e)}"}), 500
    
