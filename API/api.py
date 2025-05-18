# API/api.py (o API/routes.py)

from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Configuración de la conexión (modifica según tu servidor Azure PostgreSQL)
DB_CONFIG = {
    "host": "tuservidor.postgres.database.azure.com",
    "database": "tu_base",
    "user": "admin@tuservidor",
    "password": "tu_contraseña",
    "port": "5432",
    "sslmode": "require"
}

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

if __name__ == "__main__":
    app.run(debug=True)
