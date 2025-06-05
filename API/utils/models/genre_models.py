from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Enum, text
from utils.database.database import db

key_enum = Enum('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '-1', name='key_type')
time_signature_enum = Enum('0', '2', '3', '4', '5', '6', '7', '8', name='time_signature_type')

class Cluster(db.Model):
    
    __tablename__ = 'genre_clusters'

    cluster_id = db.Column(
        db.String(15),
        primary_key=True,
        server_default=text("'C-' || substr(md5(random()::text), 0, 12)")
    )

    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(300))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    genres = db.relationship('Genre', back_populates='cluster')

    def to_dict(self):
        return {
            "cluster_id": self.cluster_id,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    def partial_to_dict(self):
        return {
            "cluster_id": self.cluster_id,
            "name": self.name
        }

class Genre(db.Model):
    __tablename__ = 'genres'

    genre_id = db.Column(
        db.String(27),
        primary_key=True,
        server_default=text("'G-' || substr(md5(random()::text), 0, 12) || 'S-000000000000'")
    )
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(1000))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    color = db.Column(db.String(7))
    creation_year = db.Column(db.Integer)
    country_of_origin = db.Column(db.String(100))
    average_mode = db.Column(db.Numeric(3, 2))
    bpm_lower = db.Column(db.Integer)
    bpm_upper = db.Column(db.Integer)
    dominant_key = db.Column(key_enum)
    typical_volume = db.Column(db.Numeric(5, 2))
    time_signature = db.Column(time_signature_enum)
    average_duration = db.Column(db.Integer)
    is_subgenre = db.Column(db.Boolean, default=False, nullable=False)

    parent_genre_id = db.Column(db.String(27), db.ForeignKey('genres.genre_id'))
    parent_genre = db.relationship('Genre', remote_side=[genre_id])

    cluster_id = db.Column(db.String(15), db.ForeignKey('genre_clusters.cluster_id'))
    cluster = db.relationship('Cluster', back_populates='genres')

    def to_dict(self):
        return {
            "genre_id": self.genre_id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active
        }
    def partial_to_dict(self):
        return {
            "genre_id": self.genre_id,
            "name": self.name
        }
    

