from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Enum, CheckConstraint

db = SQLAlchemy()

class Cluster(db.Model):
    
    __tablename__ = 'genre_clusters'

    cluster_id = db.Column(db.String(15), primary_key=True)
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