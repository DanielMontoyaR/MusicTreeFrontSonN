import uuid
from utils.database.database import db
from flask import jsonify
from utils.database.Artist.search_artist_db import *


#p_search_term
def ejecutarBusquedaDB(text):
    try:
        if text is None:
            raise ValueError("Failed to find 'artist' object. Check input data.")
        

        result = ejecutarBusquedaDB(text)

        #print("Clúster creado con ID:", genre_id)  # Log para verificar el ID generado
        db.session.commit()
        return jsonify({
            "message": "Busqueda realizada correctamente.",
            "search": result.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error interno: {str(e)}"}), 500