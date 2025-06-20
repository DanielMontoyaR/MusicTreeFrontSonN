from utils.database.database import db
from datetime import datetime
from sqlalchemy import Enum, CheckConstraint

class Fan(db.Model):
    __tablename__ = 'fans'

    id = db.Column(db.String(24), primary_key=True)  # o Integer/UUID si prefieres
    username = db.Column(db.String(30), nullable=False, unique=True)
    fullname = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    avatar = db.Column(db.Integer, nullable=True)  # Si es ID de avatar

    favorite_genres = db.relationship(
        'Genre',
        secondary='fan_genres',
        back_populates='fans'
    )

