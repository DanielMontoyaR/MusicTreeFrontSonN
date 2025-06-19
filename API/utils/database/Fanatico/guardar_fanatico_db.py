import traceback
from utils.database.database import db
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

def guardarFanaticoDB(fanatico):
    try:
        if fanatico is None:
            return jsonify({"error": "Datos del fanático no proporcionados"}), 400

        query = text("""
            SELECT * FROM register_fan(
                :p_username,
                :p_password,
                :p_fullname,
                :p_country,
                :p_avatar_id,
                :p_genre_ids
            )
        """)

        result = db.session.execute(query, {
            'p_username': fanatico['username'],
            'p_password': fanatico['password'],
            'p_fullname': fanatico['fullname'],
            'p_country': fanatico['country'],
            'p_avatar_id': fanatico['avatar'],
            'p_genre_ids': fanatico['favorite_genres']
        })

        fan_id = result.scalar()
        db.session.commit()

        # Devolvemos directamente la respuesta JSON con el código 201
        return jsonify({
            "mensaje": "Fanático registrado exitosamente",
            "fan_id": fan_id
        }), 201

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            "error": "Restricción de integridad violada",
            "detalle": str(e)
        }), 400

    except Exception as e:
        db.session.rollback()
        print("Error en servidor:", traceback.format_exc())
        return jsonify({
            "error": "Error inesperado al registrar el fanático",
            "detalle": str(e)
        }), 500
