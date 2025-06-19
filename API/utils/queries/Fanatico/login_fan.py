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
        user = data.get('username')
        password = data.get('password')

        if not user or not password:
            return jsonify({
                "error": "Los campos 'username' y 'password' son obligatorios"
            }), 400

        result = db.session.execute(
            text("SELECT * FROM authenticate_fan(:fan_username, :fan_password)"),
            {
                'fan_username': user,
                'fan_password': password
            }
        )

        row = result.fetchone()

        if row is None:
            return jsonify({
                "error": "Credenciales incorrectas",
                "authenticated": False
            }), 401

        fan_data = {
            "message": row[4]
        }

        return jsonify({
            "authenticated": True,
            "fan": fan_data
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error interno: {str(e)}"}), 500


