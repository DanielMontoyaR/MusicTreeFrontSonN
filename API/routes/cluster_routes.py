from flask import Blueprint, request, jsonify
from utils.queries.Cluster.crear_cluster_genero import *
from utils.queries.Cluster.get_clusters_genero import *
from utils.queries.Cluster.get_clusters import *

cluster_bp = Blueprint('cluster_bp', __name__)

@cluster_bp.route('/create_cluster_genero', methods=['POST'])
def crear_cluster_genero():
    data = request.get_json()
    try:
        cluster, error_response, status_code = crearClusterGeneroData(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return guardarClusterDB(cluster)

@cluster_bp.route('/get_clusters_genero', methods=['GET'])
def obtener_clusters_genero():
    return getClusterGenero()

@cluster_bp.route('/api/get_clusters', methods=['GET'])
def obtener_clusters():
    return getClusters()
