from utils.database.database import db
from datetime import datetime
from sqlalchemy import Enum, CheckConstraint

# Enums
activity_status_enum = Enum('active', 'inactive', name='activity_status')
musical_mode_enum = Enum(
    'C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G',
    'G#/Ab', 'A', 'A#/Bb', 'B', 'none', name='musical_mode'
)

# Tabla principal de artistas
class Artist(db.Model):
    __tablename__ = 'artists'

    artist_id = db.Column(db.String(15), primary_key=True)
    status = db.Column(activity_status_enum, default='active', nullable=False)
    name = db.Column(db.String(100), nullable=False)
    biography = db.Column(db.Text)
    country_of_origin = db.Column(db.String(100))   
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    cover_image_path = db.Column(db.Text)

    __table_args__ = (
        CheckConstraint('LENGTH(name) BETWEEN 3 AND 100', name='name_length'),
    )

    albums = db.relationship('Album', backref='artist', cascade="all, delete-orphan")
    activity_years = db.relationship('ArtistActivityYear', backref='artist', cascade="all, delete-orphan")
    members = db.relationship('BandMember', backref='artist', cascade="all, delete-orphan")
    genres = db.relationship('ArtistGenre', backref='artist', cascade="all, delete-orphan")
    subgenres = db.relationship('ArtistSubgenre', backref='artist', cascade="all, delete-orphan")
    comments = db.relationship('ArtistComment', backref='artist', cascade="all, delete-orphan")
    photos = db.relationship('ArtistPhoto', backref='artist', cascade="all, delete-orphan")
    events = db.relationship('ArtistEvent', backref='artist', cascade="all, delete-orphan")

# Años de actividad
class ArtistActivityYear(db.Model):
    __tablename__ = 'artist_activity_years'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(15), db.ForeignKey('artists.artist_id', ondelete='CASCADE'), nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    end_year = db.Column(db.Integer)
    is_present = db.Column(db.Boolean, default=False)

    __table_args__ = (
        CheckConstraint(
            "(end_year IS NULL AND is_present = FALSE) OR (end_year IS NOT NULL AND end_year >= start_year) OR (is_present = TRUE)",
            name='valid_years'
        ),
    )

# Miembros de banda
class BandMember(db.Model):
    __tablename__ = 'band_members'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(15), db.ForeignKey('artists.artist_id', ondelete='CASCADE'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    instrument = db.Column(db.String(100))
    start_period = db.Column(db.String(50))
    end_period = db.Column(db.String(50))
    is_current = db.Column(db.Boolean, default=True)

# Álbumes
class Album(db.Model):
    __tablename__ = 'albums'

    album_id = db.Column(db.String(30), primary_key=True)
    artist_id = db.Column(db.String(15), db.ForeignKey('artists.artist_id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.Date)
    cover_image_path = db.Column(db.Text)
    duration_seconds = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Relaciones artista-género
class ArtistGenre(db.Model):
    __tablename__ = 'artist_genres'

    artist_id = db.Column(db.String(15), db.ForeignKey('artists.artist_id', ondelete='CASCADE'), primary_key=True)
    genre_id = db.Column(db.String(38), db.ForeignKey('genres.genre_id', ondelete='CASCADE'), primary_key=True)

# Relaciones artista-subgénero
class ArtistSubgenre(db.Model):
    __tablename__ = 'artist_subgenres'

    artist_id = db.Column(db.String(15), db.ForeignKey('artists.artist_id', ondelete='CASCADE'), primary_key=True)
    subgenre_id = db.Column(db.String(38), db.ForeignKey('genres.genre_id', ondelete='CASCADE'), primary_key=True)

# Comentarios
class ArtistComment(db.Model):
    __tablename__ = 'artist_comments'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(15), db.ForeignKey('artists.artist_id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)

# Álbum de fotos
class ArtistPhoto(db.Model):
    __tablename__ = 'artist_photos'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(15), db.ForeignKey('artists.artist_id', ondelete='CASCADE'), nullable=False)
    image_path = db.Column(db.Text, nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text)

# Eventos
class ArtistEvent(db.Model):
    __tablename__ = 'artist_events'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(15), db.ForeignKey('artists.artist_id', ondelete='CASCADE'), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

class ArtistView(db.Model):
    __tablename__ = 'artist_catalog_view'
    __table_args__ = {'info': dict(is_view = True)}

    artist_id = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country_of_origin = db.Column(db.String(100))   
    album_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(activity_status_enum, nullable=False)
    activity_years = db.Column(db.String(100))

class ArtistSearch(db.Model):
    __tablename__ = 'artist_search'

    p_search = db.Column(db.String(10000), nullable=False)
    
    
