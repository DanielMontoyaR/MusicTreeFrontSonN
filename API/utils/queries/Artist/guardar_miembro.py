import traceback
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from utils.database.database import db
from sqlalchemy import text
from utils.database.Artist.add_band_member_artist_db import add_band_member_artist_db


def guardar_miembro_individual(miembro_data, artist_id):
    try:
        if not artist_id:
            return jsonify({"error": "Artist ID inválido"}), 400

        if not miembro_data.get('nombre'):
            return jsonify({"error": "El nombre del miembro es obligatorio"}), 400

        if not miembro_data.get('instrumento'):
            return jsonify({"error": "El instrumento del miembro es obligatorio"}), 400

        # Convertir años a cadenas para coincidir con la función SQL (espera VARCHAR)
        try:
            start_period = str(int(miembro_data['desde']))
        except ValueError:
            return jsonify({"error": "El año de inicio debe ser un número válido"}), 400

        end_period_raw = miembro_data.get('hasta', None)
        is_current = bool(miembro_data.get('is_current', False))

        if isinstance(end_period_raw, str) and end_period_raw.strip().lower() == "presente":
            end_period = None
            is_current = True
        elif end_period_raw is not None:
            try:
                end_period = str(int(end_period_raw))
            except ValueError:
                return jsonify({"error": "El año de fin debe ser un número válido o 'presente'"}), 400
        else:
            end_period = None

        result = add_band_member_artist_db(artist_id, miembro_data, start_period, end_period, is_current)

        return None

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            "error": "Error de integridad al guardar el miembro",
            "detalle": str(e.orig) if hasattr(e, 'orig') else str(e)
        }), 409

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Error inesperado al guardar el miembro",
            "detalle": str(e),
            "trace": traceback.format_exc()
        }), 500



def guardarMiembro(data, artist_id):
    try:
        if data.get('is_band') is False:
            return None, None

        miembros_data = data.get('miembros', [])
        if not miembros_data:
            return None, None  # Caso sin miembros

        for miembro in miembros_data:
            error_response = guardar_miembro_individual(miembro, artist_id)
            if error_response:
                return error_response  # Esta ya es una tupla (jsonify, status)

        db.session.commit()
        return None, None

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Error al procesar miembros",
            "detalle": str(e)
        }), 500

    

