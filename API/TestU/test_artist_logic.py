import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from utils.queries.Artist.crear_artista import crearArtistaData
from utils.queries.Artist.get_artists import getArtists
from utils.queries.Artist.guardar_album import guardar_album_individual
from utils.queries.Artist.guardar_miembro import guardarMiembro
from utils.queries.Artist.search_artist import ejecutarBusquedaDB


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


# ---------------- TEST: ejecutarBusquedaDB retorna resultados ----------------
@patch("utils.queries.Artist.search_artist.db.session.execute")
def test_ejecutar_busqueda(mock_execute, app):
    mock_execute.return_value.to_dict.return_value = {"matches": ["Radiohead"]}
    text_mock = MagicMock()
    text_mock.name = "Radiohead"

    with app.app_context():
        resp, status = ejecutarBusquedaDB(text_mock)

    assert status == 201
    assert "Busqueda realizada correctamente." in resp.json["message"]
    assert "matches" in resp.json["search"]
