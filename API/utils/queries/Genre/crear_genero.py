import traceback
from utils.database.database import db
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from utils.models.genre_models import Genre
from sqlalchemy import func, text
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, BOOLEAN
from sqlalchemy import Numeric as DECIMAL

def validar_genero(data):
    if data.get("is_subgenre") and not data.get("parent_genre_id"):
        return None, jsonify({"error": "Un subgénero debe tener un 'parent_genre_id'"}), 400

    # Validar que el género padre exista si se indicó
    parent_id = data.get("parent_genre_id")
    if parent_id:
        parent = db.session.get(Genre, parent_id)
        if not parent:
            return None, jsonify({"error": f"El género padre con ID {parent_id} no existe"}), 400
    
    return None, None, None


def crearGeneroData(data):

    genero_obj, resp, status = validar_genero(data)
    if resp is not None:
        return genero_obj, resp, status

    # Validaciones clave
    if not data.get('name'):
        return None, jsonify({"error": "El nombre es obligatorio"}), 400

    if data.get('is_subgenre') and not data.get('parent_genre_id'):
        return None, jsonify({"error": "Subgéneros deben tener género padre"}), 400

    if data.get('is_subgenre') and data.get('color'):
        return None, jsonify({"error": "Subgéneros no deben tener color"}), 400

    if data.get('bpm_lower') and data.get('bpm_upper') and int(data['bpm_lower']) > int(data['bpm_upper']):
        return None, jsonify({"error": "bpm_lower no puede ser mayor que bpm_upper"}), 400

     # Conversión de tipos para asegurar consistencia con la base de datos
    try:
        if data.get('bpm_lower') is not None and data['bpm_lower'] != '':
            data['bpm_lower'] = int(data['bpm_lower'])

        if data.get('bpm_upper') is not None and data['bpm_upper'] != '':
            data['bpm_upper'] = int(data['bpm_upper'])

        if data.get('average_duration') is not None and data['average_duration'] != '':
            data['average_duration'] = int(data['average_duration'])

        if data.get('average_mode') is not None and data['average_mode'] != '':
            data['average_mode'] = float(int(data['average_mode']))

        if data.get('typical_volume') is not None and data['typical_volume'] != '':
            data['typical_volume'] = float(data['typical_volume'])

        if data.get('creation_year') is not None and data['creation_year'] != '':
            data['creation_year'] = int(data['creation_year'])

        if data.get('dominant_key') == '' or data.get('dominant_key') is None:
            data['dominant_key'] = None
        else:
            data['dominant_key'] = data['dominant_key']  # Si es ENUM tipo texto

        if data.get('time_signature') == '' or data.get('time_signature') is None:
            data['time_signature'] = None
        else:
            data['time_signature'] = data['time_signature']  # Si es ENUM tipo texto

    except ValueError as e:
        return None, jsonify({"error": "Error de formato de tipo", "detalle": str(e)}), 400

    nuevo_genero = Genre(
        name=data['name'],
        description=data.get('description'),
        is_active=data.get('is_active'),
        color=data.get('color'),
        creation_year=data.get('creation_year'),
        country_of_origin=data.get('country_of_origin'),
        average_mode=data.get('average_mode'),
        bpm_lower=data.get('bpm_lower'),
        bpm_upper=data.get('bpm_upper'),
        dominant_key=data.get('dominant_key'),
        typical_volume=data.get('typical_volume'),
        time_signature=data.get('time_signature'),
        average_duration=data.get('average_duration'),
        is_subgenre=data.get('is_subgenre'),
        parent_genre_id=data.get('parent_genre_id'),
        cluster_id=data.get('cluster_id')
    )    

    return nuevo_genero, None, None





