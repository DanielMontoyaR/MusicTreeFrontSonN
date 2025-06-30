import uuid
from utils.database.database import db
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, text
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, BOOLEAN
from sqlalchemy import Numeric as DECIMAL


#p_search_term
def ejecutarBusquedaDB(text):
    try:
        if text is None:
            raise ValueError("Failed to find 'artist' object. Check input data.")

        query = text("""
            SELECT search_artist_json(
                :p_search_term
            )
        """)

        # Execute with type hints in the parameters dictionary
        result = db.session.execute(
            query,
            {
                'p_search_term': text.name,
            }
        )

        #print("Clúster creado con ID:", genre_id)  # Log para verificar el ID generado
        db.session.commit()
        return jsonify({
            "message": "Busqueda realizada correctamente.",
            "search": result.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error interno: {str(e)}"}), 500