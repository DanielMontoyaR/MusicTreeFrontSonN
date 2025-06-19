import traceback
from utils.database.database import db
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, text
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, BOOLEAN
from sqlalchemy import Numeric as DECIMAL

def loginFanData(data):
    try:
        # Validaciones (movidas desde el endpoint)
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

        # Lógica de autenticación
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

        fan_data = {
            "mensaje": f"Bienvenido, {user}",
        }

        return {
            "authenticated": True,
            "detalle": "Sesión iniciada correctamente",
            "fan": fan_data
        }, None, None

    except Exception as e:
        db.session.rollback()
        return None, jsonify({
            "error": "Error interno del servidor",
            "detalle": str(e),
            "trace": traceback.format_exc()
        }), 500


