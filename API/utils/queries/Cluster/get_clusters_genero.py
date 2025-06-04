from flask import jsonify
from sqlalchemy.exc import IntegrityError
from utils.models.models import Cluster

def getClusterGenero():
    try:
        clusters = Cluster.query.all()
        clusters_json = [cluster.to_dict() for cluster in clusters]
        return jsonify(clusters_json), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener los clusters: {str(e)}"}), 500