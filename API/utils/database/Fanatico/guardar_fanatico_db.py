import traceback
from utils.database.database import db
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

def guardarFanaticoDB(fanatico):
    try:
        if fanatico is None:
            raise ValueError("No se pudo crear el objeto 'fanatico'. Verifique los datos de entrada.")

        query = text("""
            SELECT register_fan(
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
            'p_avatar_id': fanatico['avatar_id'],
            'p_genre_ids': fanatico['favorite_genres']
        })

        fan_id = result.scalar()
        db.session.commit()

        return None, fan_id

    except IntegrityError as e:
        db.session.rollback()
        error_response = jsonify({
            "error": "Restricción de integridad violada",
            "detalle": str(e)
        })
        return error_response, None

    except Exception as e:
        db.session.rollback()
        print("Error en servidor:", traceback.format_exc())
        error_response = jsonify({
            "error": "Error inesperado al registrar el fanático",
            "detalle": str(e)
        })
        return error_response, None
