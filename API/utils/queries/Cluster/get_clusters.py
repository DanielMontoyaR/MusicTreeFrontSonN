from flask import jsonify
from sqlalchemy.exc import IntegrityError
from API.utils.models.genre_models import Cluster

def getClusters():
    try:
        clusters = Cluster.query.filter_by(is_active=True).all()
        clusters_json = [cluster.partial_to_dict() for cluster in clusters]
        return jsonify(clusters_json), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener los clusters: {str(e)}"}), 500