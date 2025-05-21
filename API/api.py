# API/api.py (o API/routes.py)

from flask import Flask, jsonify, request
from utils.models import *
from utils.queries import *
from sqlalchemy.exc import IntegrityError
import uuid


app = Flask(__name__)

# Configuración para conectarte a Azure PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://musictreeadmin:AxpHDxGS2BcFdaf@musictree-server.postgres.database.azure.com:5432/postgres?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
     clusters = GenreCluster.query.all()
     
     return jsonify([c.to_dict() for c in clusters])


@app.route('/create_cluster_genero', methods=['POST'])
def crear_cluster_genero():
    data = request.get_json()

    name = data.get('name')
    description = data.get('description', '')

    if not name:
        return jsonify({"error": "El campo 'name' es obligatorio."}), 400

    # Crear un ID único limitado a 15 caracteres
    cluster_id = str(uuid.uuid4())[:15]

    nuevo_cluster = GenreCluster(
        cluster_id=cluster_id,
        name=name,
        description=description,
        created_at=datetime.now(datetime.timezone.utc)
    )

    try:
        db.session.add(nuevo_cluster)
        db.session.commit()
        return jsonify({
            "message": "Cluster creado correctamente.",
            "cluster": nuevo_cluster.to_dict()
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Ya existe un cluster con ese nombre."}), 409

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

@app.route('/get_clusters_genero', methods=['GET'])
def obtener_clusters_genero():
    try:
        clusters = GenreCluster.query.all()
        clusters_json = [cluster.to_dict() for cluster in clusters]
        return jsonify(clusters_json), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener los clusters: {str(e)}"}), 500

"""

    





# Endpoint para verificar credenciales
@app.route("/verificar_credenciales", methods=["POST"])
def verificar():
    data = request.json
    usuario = data.get("usuario")
    contraseña = data.get("contraseña")

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s AND contraseña = %s", (usuario, contraseña))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            return jsonify({"autenticado": True}), 200
        else:
            return jsonify({"autenticado": False}), 401
    except Exception as e:
        print("Error al verificar credenciales:", e)
        return jsonify({"error": "Error interno"}), 500
"""

# --- POST /api/genres ---
@app.route('/api/create_genres', methods=['POST'])
def crear_genero():
    data = request.get_json()

    # Validaciones clave
    if not data.get('name'):
        return jsonify({"error": "El nombre es obligatorio"}), 400

    if data.get('is_subgenre') and not data.get('parent_genre_id'):
        return jsonify({"error": "Subgéneros deben tener género padre"}), 400

    if data.get('is_subgenre') and data.get('color'):
        return jsonify({"error": "Subgéneros no deben tener color"}), 400

    if data.get('bpm_lower') and data.get('bpm_upper') and data['bpm_lower'] > data['bpm_upper']:
        return jsonify({"error": "bpm_lower no puede ser mayor que bpm_upper"}), 400
    
    if not data.get('cluster.id'):
        return jsonify({"error": "Se debe especificar el cluster"}), 400

    try:
        genre_id = generar_genre_id(data.get('is_subgenre', False))

        nuevo_genero = Genre(
            genre_id=genre_id,
            name=data['name'],
            description=data.get('description'),
            is_active=data.get('is_active', True),
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
            is_subgenre=data.get('is_subgenre', False),
            parent_genre_id=data.get('parent_genre_id'),
            cluster_id=data.get('cluster_id')
        )

        db.session.add(nuevo_genero)
        db.session.commit()

        return jsonify({
            "mensaje": "Género creado exitosamente",
            "genre_id": nuevo_genero.genre_id
        }), 201

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Restricción de integridad violada", "detalle": str(e)}), 409

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error inesperado", "detalle": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
