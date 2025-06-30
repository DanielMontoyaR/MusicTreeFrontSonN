import traceback
from utils.database.database import db
from flask import jsonify

def validar_rate_artist(data):
    fan_id = data.get("fan_id")
    artist_id = data.get("artist_id")
    rating = data.get("rating")

    if fan_id is None or artist_id is None or rating is None:
        return jsonify({"error": "Se requieren fan_id, artist_id y rating"}), 400

    try:
        fan_id = int(fan_id)
        rating = int(rating)
    except ValueError:
        return jsonify({"error": "fan_id y rating deben ser enteros"}), 400

    if not (1 <= rating <= 5):
        return jsonify({"error": "El rating debe estar entre 1 y 5"}), 400

    return None, {
        "fan_id": fan_id,
        "artist_id": artist_id,
        "rating": rating
    }