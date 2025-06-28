import traceback
from utils.database.database import db
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

def autenticar_fan_en_db(username, password):
    result = db.session.execute(
        text("SELECT * FROM authenticate_fan(:fan_username, :fan_password)"),
        {"fan_username": username, "fan_password": password}
    )
    return result.fetchone()