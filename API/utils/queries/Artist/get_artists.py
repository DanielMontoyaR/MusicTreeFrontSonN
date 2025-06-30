from flask import jsonify
from sqlalchemy import text
from utils.database.database import db
from utils.logging.logger import configurar_logger

def getArtists():
    logger = configurar_logger()
    try:
        # Execute raw SQL to select from the view
        result = db.session.execute(text("SELECT * FROM artist_catalog_view"))  # Replace with your view name
        
        # Convert result to list of dicts
        artists = [dict(row._mapping) for row in result]
        
        return jsonify(artists)
            
        
    except Exception as e:
        logger.error("Error en loginFanData: %s", str(e), exc_info=True)
        db.session.rollback()
        return jsonify({"error": f"Error interno: {str(e)}"}), 500
    
