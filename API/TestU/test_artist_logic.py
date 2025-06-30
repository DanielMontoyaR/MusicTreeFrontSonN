import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from utils.queries.Artist.crear_artista import crearArtistaData
from utils.queries.Artist.get_artists import getArtists
from utils.queries.Artist.guardar_album import guardar_album_individual
from utils.queries.Artist.guardar_miembro import guardarMiembro
from utils.queries.Artist.search_artist import ejecutarBusquedaDB
from utils.queries.Artist.rate_artist import *
from utils.queries.Artist.get_perfil_artista import obtenerPerfilArtista


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    return app


# ---------------- TEST: crearArtistaData válido ----------------
def test_crear_artista_valido(app):
    data = {
        "nombre": "Radiohead",
        "pais": "UK",
        "año_desde": "1990",
        "año_hasta": "presente",
        "genre_ids": ["1", "2"],
        "subgenre_ids": ["3"],
        "biografia": "Una banda legendaria",
    }

    with app.app_context():
        artista, resp, status = crearArtistaData(data)

    assert artista is not None
    assert artista["name"] == "Radiohead"
    assert resp is None
    assert status is None


# ---------------- TEST: getArtists mockeando query SQL ----------------
@patch("utils.queries.Artist.get_artists.db.session.execute")
def test_get_artists(mock_execute, app):
    mock_execute.return_value = [MagicMock(_mapping={"name": "Radiohead"})]

    with app.app_context():
        resp = getArtists()

    assert isinstance(resp.json, list)
    assert resp.json[0]["name"] == "Radiohead"


# ---------------- TEST: guardar_album_individual válido ----------------
@patch("utils.queries.Artist.guardar_album.db.session.execute")
def test_guardar_album_individual(mock_execute, app):
    mock_execute.return_value.scalar.return_value = "album-id-123"

    album_data = {
        "titulo": "OK Computer",
        "año": "1997",
        "cover_image_path": "cover.jpg",
        "duration_seconds": 3600
    }

    with app.app_context():
        album_id, error = guardar_album_individual(album_data, "artist-id-123")

    assert album_id == "album-id-123"
    assert error is None


# ---------------- TEST: guardarMiembro con datos válidos ----------------
@patch("utils.queries.Artist.guardar_miembro.db.session.execute")
def test_guardar_miembro(mock_execute, app):
    data = {
        "is_band": True,
        "miembros": [
            {
                "nombre": "Thom Yorke",
                "instrumento": "Voz",
                "desde": "1990",
                "hasta": "presente",
                "is_current": True
            }
        ]
    }

    with app.app_context():
        error_response, _ = guardarMiembro(data, "artist-id-123")

    assert error_response is None

# --------- CASO CORRECTO DE VALIDACIÓN ----------
def test_validar_rate_artist_valido():
    data = {"fan_id": 1, "artist_id": "A-123", "rating": 5}
    error_response, status_code, valid_data = validar_rate_artist(data)

    assert error_response is None
    assert status_code is None
    assert valid_data == {"fan_id": 1, "artist_id": "A-123", "rating": 5}


# ----------- CASO ÉXITO -----------
@patch("utils.queries.Artist.get_perfil_artista.obtenerPerfilArtistaCompleto")
def test_obtener_perfil_artista_exito(mock_obtener, app):
    mock_row = MagicMock()
    mock_row._mapping = {"name": "Radiohead", "id": "A-123"}
    
    mock_result = MagicMock()
    mock_result.fetchone.return_value = mock_row
    mock_obtener.return_value = mock_result

    with app.app_context():
        perfil, error_response, status_code = obtenerPerfilArtista({"artist_id": "A-123"})

    assert error_response is None
    assert status_code is None
    assert perfil["name"] == "Radiohead"


# ----------- CASO FALTA ID -----------
def test_obtener_perfil_artista_sin_id(app):
    with app.app_context():
        perfil, error_response, status_code = obtenerPerfilArtista({})

    assert perfil is None
    assert status_code == 400
    assert "artist_id" in error_response.json["error"]


# ----------- CASO ARTISTA NO EXISTE -----------
@patch("utils.queries.Artist.get_perfil_artista.obtenerPerfilArtistaCompleto")
def test_obtener_perfil_artista_no_encontrado(mock_obtener, app):
    mock_result = MagicMock()
    mock_result.fetchone.return_value = None
    mock_obtener.return_value = mock_result

    with app.app_context():
        perfil, error_response, status_code = obtenerPerfilArtista({"artist_id": "no-existe"})

    assert perfil is None
    assert status_code == 404
    assert "no encontrado" in error_response.json["error"]


# ----------- CASO EXCEPCIÓN INTERNA -----------
@patch("utils.queries.Artist.get_perfil_artista.obtenerPerfilArtistaCompleto")
def test_obtener_perfil_artista_excepcion(mock_obtener, app):
    mock_obtener.side_effect = Exception("fallo de base de datos")

    with app.app_context():
        perfil, error_response, status_code = obtenerPerfilArtista({"artist_id": "A-123"})

    assert perfil is None
    assert status_code == 500
    assert "Error interno" in error_response.json["error"]
    assert "fallo de base de datos" in error_response.json["detalle"]