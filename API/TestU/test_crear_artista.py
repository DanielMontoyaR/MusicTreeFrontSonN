import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from utils.queries.Artist.crear_artista import crearArtistaData



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

    