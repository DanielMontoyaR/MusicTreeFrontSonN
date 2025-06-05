# API/api.py (o API/routes.py)
from flask import Flask, jsonify, request
from utils.database.database import db
from utils.queries.Cluster.crear_cluster_genero import *
from utils.queries.Cluster.get_clusters_genero import *
from utils.queries.Genre.crear_genero import *
from utils.queries.Genre.get_generos import *
from utils.queries.Cluster.get_clusters import *
from utils.queries.Artist.crear_artista import *
from utils.queries.Artist.guardar_album import *

app = Flask(__name__)

# Configuración para conectarte a Azure PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://musictreeadmin:AxpHDxGS2BcFdaf@musictree-server.postgres.database.azure.com:5432/postgres?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/create_cluster_genero', methods=['POST'])
def crear_cluster_genero():
    data = request.get_json()

    try:

        cluster, error_response, status_code = crearClusterGeneroData(data)

    except Exception as e:
        error_response = {"error": str(e)}  # Ensure this is a dictionary
        status_code = 500
        return jsonify(error_response), status_code

    return guardarClusterDB(cluster)

@app.route('/get_clusters_genero', methods=['GET'])
def obtener_clusters_genero():

    return getClusterGenero()
#cambio para vcer

#Endpoint para crear géneros
@app.route('/api/create_genres', methods=['POST'])
def crear_genero():
    data = request.get_json()

    try:
        genero, error_response, status_code = crearGeneroData(data)

    except Exception as e:
        error_response = {"error": str(e)}  # Ensure this is a dictionary
        status_code = 500
        return jsonify(error_response), status_code

    return guardarGeneroDB(genero)

@app.route('/api/get_genres', methods=['GET'])
def obtener_generos():
    return getGeneros()

@app.route('/api/get_clusters', methods=['GET'])
def obtener_clusters():
    return getClusters()

@app.route('/api/crear_artista_completo', methods=['POST'])
def crear_artista_completo():
    data = request.get_json()

    try:
        # Paso 1: Validar y preparar datos
        artista_data, error_response, status_code = crearArtistaData(data)
        if error_response:
            return error_response, status_code

        # Paso 2: Guardar artista → obtener ID
        error_response, artist_id = guardarArtistaDB(artista_data)
        if error_response:
            return error_response, 400  # O el código de estado apropiado

        # Paso 3: Procesar álbumes
        album_ids, error_response = guardar_albumes(data, artist_id)
        if error_response:
            return error_response, 400

        # Paso 4: Si es banda, guardar miembros
        if data.get('is_band', False):
            miembros = data.get('members', [])
            for miembro in miembros:
                guardarMiembroDB(miembro, artist_id)

        return jsonify({
            "mensaje": "Artista, álbumes y miembros registrados exitosamente.",
            "artist_id": artist_id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Error inesperado en el registro completo",
            "detalle": str(e)
        }), 500

    

if __name__ == "__main__":
    app.run(port=5000,debug=True)
