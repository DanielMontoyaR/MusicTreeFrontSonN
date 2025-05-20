# API/api.py (o API/routes.py)

from flask import Flask, jsonify, request
from utils.models import *
from utils.queries import *
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)

# Configuración para conectarte a Azure PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://musictreeadmin:AxpHDxGS2BcFdaf@musictree-server.postgres.database.azure.com:5432/postgres?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
     clusters = GenreCluster.query.all()
     
     return jsonify([c.to_dict() for c in clusters])



"""
@app.route("/crear_cluster_gen", methods=["POST"])
def crear_cluster():
    data = request.json
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")
    fecha = data.get("fecha")
    hora = data.get("hora")

    if not nombre:
        return jsonify({"error": "El nombre es obligatorio"}), 400

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO genero_cluster (nombre, descripcion, fecha, hora)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        ''', (nombre, descripcion, fecha, hora))
        cluster_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Cluster creado", "id": cluster_id}), 201
    except Exception as e:
        print("Error al crear cluster:", e)
        return jsonify({"error": "Error interno"}), 500
    


@app.route("/clusters_genero", methods=["GET"])
def obtener_clusters_genero():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, descripcion, fecha, hora FROM genero_cluster")
        resultados = cursor.fetchall()
        conn.close()

        clusters = []
        for fila in resultados:
            clusters.append({
                "id": fila[0],
                "nombre": fila[1],
                "descripcion": fila[2],
                "fecha": str(fila[3]),
                "hora": str(fila[4])
            })

        return jsonify(clusters), 200

    except Exception as e:
        print("Error al obtener clusters:", e)
        return jsonify({"error": "Error interno"}), 500


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
@app.route('/api/genres', methods=['POST'])
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
