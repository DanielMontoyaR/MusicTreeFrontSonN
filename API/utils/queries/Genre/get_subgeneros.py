from flask import jsonify
from sqlalchemy.exc import IntegrityError
from utils.models.genre_models import Genre

def getSubGeneros():
    try:
        genres = Genre.query.filter_by(is_subgenre=True).all()
        genre_json = [genre.partial_to_dict() for genre in genres]
        return jsonify(genre_json), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener los clusters: {str(e)}"}), 500