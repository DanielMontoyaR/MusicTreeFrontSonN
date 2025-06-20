import uuid
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from utils.database.database import db
from utils.models.genre_models import Cluster
from sqlalchemy import func, text
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, BOOLEAN
from sqlalchemy import Numeric as DECIMAL


def guardarClusterDB(cluster):
    try:
        if cluster is None:
            raise ValueError("Failed to create 'cluster' object. Check input data.")

        query = text("""
            SELECT create_genre_cluster(
                :name, :description, :is_active
            )
        """)

        # Execute with type hints in the parameters dictionary
        result = db.session.execute(
            query,
            {
                'name': cluster.name,
                'description': cluster.description,
                'is_active': cluster.is_active,
            }
        )

        #print("Clúster creado con ID:", genre_id)  # Log para verificar el ID generado
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