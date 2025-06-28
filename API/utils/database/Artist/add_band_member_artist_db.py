import traceback
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from utils.database.database import db
from sqlalchemy import text

def add_band_member_artist_db(artist_id, miembro_data, start_period, end_period, is_current):
    # Ejecutar función PostgreSQL con parámetros exactos
    query = text("""
        SELECT add_band_member(
            :p_artist_id,
            :p_full_name,
            :p_instrument,
            :p_start_period,
            :p_end_period,
            :p_is_current
        )
    """)

    result = db.session.execute(query, {
        'p_artist_id': artist_id,
        'p_full_name': miembro_data['nombre'],
        'p_instrument': miembro_data['instrumento'],
        'p_start_period': start_period,
        'p_end_period': end_period,
        'p_is_current': is_current,
    })

    return result