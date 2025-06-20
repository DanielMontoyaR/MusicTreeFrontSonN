from flask import Flask
from utils.database.database import db
from routes.cluster_routes import cluster_bp
from routes.genre_routes import genre_bp
from routes.artist_routes import artist_bp
from routes.fan_routes import fan_bp

app = Flask(__name__)

# Configuración para conectarte a Azure PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://musictreeadmin:AxpHDxGS2BcFdaf@musictree-server.postgres.database.azure.com:5432/postgres?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Registrar Blueprints
app.register_blueprint(cluster_bp)
app.register_blueprint(genre_bp)
app.register_blueprint(artist_bp)
app.register_blueprint(fan_bp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
