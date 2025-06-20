import uuid
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from utils.models.genre_models import Cluster
from sqlalchemy import func, text
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, BOOLEAN
from sqlalchemy import Numeric as DECIMAL

def crearClusterGeneroData(data):
    name = data.get('name')
    description = data.get('description', '')
    is_active = data.get('is_active')

    if not name:
        return None, {"error": "El campo 'name' es obligatorio."}, 400

    nuevo_cluster = Cluster(
        name=name,
        description=description,
        is_active=is_active
    )
    return nuevo_cluster, None, None


    