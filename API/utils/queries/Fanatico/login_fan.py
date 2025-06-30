import traceback
from flask import jsonify
from sqlalchemy import text
from utils.database.database import db

def loginFanData(data):
    try:
        # Validación básica
        if not data:
            return None, jsonify({
                "error": "Los campos 'username' y 'password' son obligatorios"
            }), 400

        user = data.get('username')
        password = data.get('password')

        if not user or not password:
            return None, jsonify({
                "error": "Los campos 'username' y 'password' son obligatorios"
            }), 400

        # Ejecutar función SQL
        result = db.session.execute(
            text("SELECT * FROM authenticate_fan(:fan_username, :fan_password)"),
            {
                'fan_username': user,
                'fan_password': password
            }
        )

        row = result.fetchone()

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

        # Mensaje inesperado
        return None, jsonify({
            "error": "Estado desconocido: " + status_message
        }), 500

    except Exception as e:
        db.session.rollback()
        return None, jsonify({
            "error": "Error interno del servidor",
            "detalle": str(e),
            "trace": traceback.format_exc()
        }), 500
