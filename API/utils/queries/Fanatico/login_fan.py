import traceback
from flask import jsonify
from sqlalchemy import text
from utils.database.database import db
from utils.database.Fanatico.login_fanatico_db import autenticar_fan_en_db

def validar_login_data(data):
    if not data:
        return jsonify({"error": "Los campos 'username' y 'password' son obligatorios"}), 400

    user = data.get('username')
    password = data.get('password')

    if not user or not password:
        return jsonify({"error": "Los campos 'username' y 'password' son obligatorios"}), 400

    return None, {"username": user, "password": password}


def loginFanData(data):
    try:
        error_response, valores = validar_login_data(data)
        if error_response:
            return None, error_response, 400

        username = valores["username"]
        password = valores["password"]

        row = autenticar_fan_en_db(username, password)

        if row is None:
            return None, jsonify({
                "error": "Credenciales incorrectas",
                "authenticated": False
            }), 401

        fan_id, full_name, country, avatar_path, status_message = row

        if status_message == "Contraseña incorrecta":
            return None, jsonify({
                "error": "Contraseña incorrecta",
                "authenticated": False
            }), 401

        if status_message == "Autenticación exitosa":
            fan_data = {
                "fan_id": fan_id,
                "full_name": full_name,
                "country": country,
                "avatar_path": avatar_path,
                "status_message": status_message
            }

            return {
                "authenticated": True,
                "detalle": "Sesión iniciada correctamente",
                "fan": fan_data
            }, None, None

        return None, jsonify({"error": "Estado desconocido: " + status_message}), 500

    except Exception as e:
        db.session.rollback()
        return None, jsonify({
            "error": "Error interno del servidor",
            "detalle": str(e),
            "trace": traceback.format_exc()
        }), 500
