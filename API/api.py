# API/api.py (o API/routes.py)
from flask import Flask, jsonify, request
from sqlalchemy.exc import IntegrityError
from utils.database.database import db
from utils.queries.Cluster.crear_cluster_genero import *
from utils.queries.Cluster.get_clusters_genero import *
from utils.queries.Genre.crear_genero import *

app = Flask(__name__)

# Configuración para conectarte a Azure PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://musictreeadmin:AxpHDxGS2BcFdaf@musictree-server.postgres.database.azure.com:5432/postgres?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/create_cluster_genero', methods=['POST'])
def crear_cluster_genero():
    data = request.get_json()

    cluster, error_response, status_code = crearClusterGeneroData(data)

    if error_response:
        return jsonify(error_response), status_code

    return guardarClusterDB(cluster)

@app.route('/get_clusters_genero', methods=['GET'])
def obtener_clusters_genero():

    return getClusterGenero()

#Endpoint para crear géneros
@app.route('/api/create_genres', methods=['POST'])
def crear_genero():
    data = request.get_json()

    genero, error_response, status_code = crearGeneroData(data)

    if error_response:
        return jsonify(error_response), status_code
    

    return guardarGeneroDB(genero)

if __name__ == "__main__":
    app.run(port=5000,debug=True)
