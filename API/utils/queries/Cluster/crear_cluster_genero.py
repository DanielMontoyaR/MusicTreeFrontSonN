import uuid
from utils.database.database import db
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from utils.models.Cluster import cluster_model

def crearClusterGeneroData(data):
    name = data.get('name')
    description = data.get('description', '')
    is_active = data.get('is_active', True)

    if not name:
        return None, {"error": "El campo 'name' es obligatorio."}, 400

    cluster_id = str(uuid.uuid4())[:15]

    nuevo_cluster = cluster_model(
        cluster_id=cluster_id,
        name=name,
        description=description,
        is_active=is_active
    )
    return nuevo_cluster, None, None

def guardarClusterDB(cluster):
    try:
        db.session.add(cluster)
        db.session.commit()
        return jsonify({
            "message": "Cluster creado correctamente.",
            "cluster": cluster.to_dict()
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Ya existe un cluster con ese nombre."}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error interno: {str(e)}"}), 500
    