# API/api.py (o API/routes.py)
from flask import Flask, jsonify, request
from utils.database.database import db
from utils.database.Fanatico.guardar_fanatico_db import *
from utils.queries.Cluster.crear_cluster_genero import *
from utils.queries.Cluster.get_clusters_genero import *
from utils.queries.Genre.crear_genero import *
from utils.queries.Genre.get_generos import *
from utils.queries.Genre.get_subgeneros import *
from utils.queries.Cluster.get_clusters import *
from utils.queries.Artist.crear_artista import *
from utils.queries.Artist.guardar_album import *
from utils.queries.Artist.guardar_miembro import *
from utils.queries.Artist.guardar_miembro import *
from utils.queries.Genre.importjsongenre import *
from utils.queries.Artist.get_artists import *
from utils.queries.Artist.search_artist import *
from utils.queries.Fanatico.login_fan import *
from utils.queries.Fanatico.crear_fanatico import *
from utils.queries.Fanatico.filtrar_artistas import *

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
        error_response = {"error": str(e)}  
        status_code = 500
        return jsonify(error_response), status_code

    return guardarClusterDB(cluster)
    

@app.route('/get_clusters_genero', methods=['GET'])
def obtener_clusters_genero():

    return getClusterGenero()


@app.route('/api/create_genres', methods=['POST'])
def crear_genero():
    data = request.get_json()

    try:
        genero, error_response, status_code = crearGeneroData(data)

    except Exception as e:
        error_response = {"error": str(e)}  
        status_code = 500
        return jsonify(error_response), status_code

    return guardarGeneroDB(genero)

@app.route('/api/procesar-generos', methods=['POST'])
def procesar_generos():
    
    data = request.get_json() 

    try:
        
        resultado, error_response, status_code  = procesar_generos_batch(data)
        if error_response:
            return error_response, status_code
        
    except Exception as e:
        error_response = {
            "error": "Error al procesar el batch de géneros",
            "detalle": str(e)
        }
        return jsonify(error_response), 500
    
    return jsonify(resultado), status_code


@app.route('/api/get_genres', methods=['GET'])
def obtener_generos():
    return getGeneros()

@app.route('/api/get_subgenres', methods=['GET'])
def obtener_subgeneros():
    return getSubGeneros()

@app.route('/api/get_clusters', methods=['GET'])
def obtener_clusters():
    return getClusters()

#Crear artista nuevo
@app.route('/api/crear_artista_completo', methods=['POST'])
def crear_artista_completo():
    data = request.get_json()

    try:
        artista_data, error_response, status_code = crearArtistaData(data)
        if error_response:
            return error_response, status_code

        error_response, artist_id = guardarArtistaDB(artista_data)
        if error_response:
            return error_response, 400  


        album_ids, error_response = guardar_albumes(data, artist_id)
        if error_response:
            return error_response, 400  


        error_response, status_code = guardarMiembro(data, artist_id)
        if error_response:
            return error_response, status_code

        return jsonify({
            "mensaje": "Artista, álbumes y miembros registrados exitosamente.",
            "artist_id": artist_id
        }), 201

    except Exception as e:
        db.session.rollback()
        error_response = {"error": str(e)}
        status_code = 500
        return jsonify(error_response), status_code

@app.route('/api/artists_view')
def get_artist_view():
    return getArtists()

@app.route('/api/search_artist', methods=['POST'])
def buscar_artista():
    data = request.get_json()

    try:
        search_term = data.get('search')

        if not search_term:
            return jsonify({"error": "Falta el parámetro 'search'"}), 400

        result = db.session.execute(
            text("SELECT * FROM search_artist_json(:search_term)"),
            {"search_term": search_term}
        )

    
        artists = [dict(row._mapping) for row in result]

        return jsonify(artists)

    except Exception as e:
        error_response = {"error": str(e)}
        status_code = 500
        return jsonify(error_response), status_code

@app.route('/api/login_fan', methods=['POST'])    
def login_fan():
    data = request.get_json()
    
    try:
        result, error_response, status_code = loginFanData(data)
        if error_response:
            return error_response, status_code
            
        return jsonify(result), 200

    except Exception as e:
        db.session.rollback()
        error_response = {"error": str(e)}  
        status_code = 500
        return jsonify(error_response), status_code

@app.route('/api/registro_fanatico', methods=['POST'])
def crear_fanatico():
    data = request.get_json()

    try:
        fanaticoData, error_response, status_code = crearFanatico(data)
        if error_response:
            return error_response, status_code

        return guardarFanaticoDB(fanaticoData)

    except Exception as e:
        error_response = {"error": str(e)}  
        status_code = 500
        return jsonify(error_response), status_code
    
@app.route('/api/filtrar_artistas', methods=['POST'])
def filtrar_artistas():
    data = request.get_json()

    try:
        resultado, error_response, status_code = buscarArtistasFiltrados(data)
        if error_response:
            return error_response, status_code

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({
            "error": "Error inesperado al procesar la solicitud",
            "detalle": str(e)
        }), 500 


if __name__ == "__main__":
    app.run(port=5000,debug=True)
