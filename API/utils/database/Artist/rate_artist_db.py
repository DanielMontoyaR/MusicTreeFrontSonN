from sqlalchemy import text
from flask import jsonify
from utils.database.database import db
from utils.logging.logger import configurar_logger
import traceback

<<<<<<< HEAD
logger = configurar_logger()

def ejecutar_rate_artist_DB(valid_data):
=======
<<<<<<< HEAD
def ejecutar_rate_artist_DB(fan_id, artist_id, rating):
>>>>>>> API
    try:
        result = db.session.execute(
            text("SELECT * FROM rate_artist(:p_fan_id, :p_artist_id, :p_rating)"),
            {
                "p_fan_id": valid_data["fan_id"],
                "p_artist_id": valid_data["artist_id"],
                "p_rating": valid_data["rating"]
            }
        )
        row = result.fetchone()
        if row is None:
            return jsonify({"error": "No se obtuvo respuesta de la base de datos"}), 500

        json_result = row[0]
        if json_result.get("status") == "error":
            return jsonify(json_result), 400

        return jsonify(json_result), 200

    except Exception as e:
        db.session.rollback()
<<<<<<< HEAD
=======
        print(f"Error al calificar artista: {e}")
        return None
=======
logger = configurar_logger()

def ejecutar_rate_artist_DB(valid_data):
    try:
        result = db.session.execute(
            text("SELECT * FROM rate_artist(:fan_id, :artist_id, :rating)"),
            {
                "fan_id": valid_data["fan_id"],
                "artist_id": valid_data["artist_id"],
                "rating": valid_data["rating"]
            }
        )
        row = result.fetchone()
        if row is None:
            return jsonify({"error": "No se obtuvo respuesta de la base de datos"}), 500

        json_result = row[0]
        if json_result.get("status") == "error":
            return jsonify(json_result), 400

        return jsonify(json_result), 200

    except Exception as e:
        db.session.rollback()
>>>>>>> API
        logger.error(f"Error en rate_artist: {e}")
        return jsonify({
            "error": "Error en la base de datos",
            "detalle": str(e),
            "trace": traceback.format_exc()
<<<<<<< HEAD
        }), 500
=======
        }), 500
>>>>>>> API_CalificarArtista
>>>>>>> API
