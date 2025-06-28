from flask import jsonify
from sqlalchemy import text
from utils.database.database import db

def getArtists():
    try:
        # Execute raw SQL to select from the view
        result = db.session.execute(text("SELECT * FROM artist_catalog_view"))  # Replace with your view name
        
        # Convert result to list of dicts
        artists = [dict(row._mapping) for row in result]
        
        return jsonify(artists)
            
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error interno: {str(e)}"}), 500
    
