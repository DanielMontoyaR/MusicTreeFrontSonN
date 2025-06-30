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



# Fallo: Error inesperado en base de datos
@patch("utils.queries.Artist.guardar_miembro.db.session.execute")
def test_guardar_miembro_db_fail(mock_execute, app):
    mock_execute.side_effect = Exception("DB error")

    data = {
        "is_band": True,
        "miembros": [{
            "nombre": "Thom Yorke",
            "instrumento": "Voz",
            "desde": "1990",
            "hasta": "presente",
            "is_current": True
        }]
    }

    with app.app_context():
        error_response, _ = guardarMiembro(data, "artist-id-123")

    assert error_response is not None
    assert error_response.status_code == 200


