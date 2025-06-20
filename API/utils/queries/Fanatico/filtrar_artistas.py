# services/artista_consultas.py

import traceback
from flask import jsonify
from sqlalchemy import text
from utils.database.database import db

def buscarArtistasFiltrados(data):
    try:
        genre_id = data.get('genre_id')
        subgenre_id = data.get('subgenre_id', '')
        nombre = data.get('nombre', '')
        limite = data.get('limite', 50)

        # Validaciones
        if not genre_id:
            return None, jsonify({"error": "El campo 'genre_id' es obligatorio"}), 400

        try:
            limite = int(limite)
        except ValueError:
            return None, jsonify({"error": "El campo 'limite' debe ser un número entero"}), 400

        # Ejecutar función SQL
        query = text("""
            SELECT * FROM search_artists_by_genre(
                :p_genre_id,
                :p_subgenre_id,
                :p_name_filter,
                :p_limit
            )
        """)

        result = db.session.execute(query, {
            'p_genre_id': genre_id,
            'p_subgenre_id': subgenre_id,
            'p_name_filter': nombre,
            'p_limit': limite
        })

        artistas = [dict(row._mapping) for row in result]

        return artistas, None, None

    except Exception as e:
        db.session.rollback()
        return None, jsonify({
            "error": "Error inesperado al consultar artistas",
            "detalle": str(e),
            "trace": traceback.format_exc()
        }), 500
