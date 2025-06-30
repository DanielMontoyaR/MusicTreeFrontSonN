import pytest
from unittest.mock import patch, MagicMock
from flask import Flask

from utils.queries.Artist.search_artist import ejecutarBusquedaDB


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    return app

# ---------------- TEST: ejecutarBusquedaDB retorna resultados ----------------
@patch("utils.queries.Artist.search_artist.db.session.execute")
def test_ejecutar_busqueda(mock_execute, app):
    mock_execute.return_value.to_dict.return_value = {"matches": ["Slash"]}
    text_mock = MagicMock()
    text_mock.name = "Slash"

    with app.app_context():
        resp, status = ejecutarBusquedaDB(text_mock)

    assert status == 201
    assert "Busqueda realizada correctamente." in resp.json["message"]
    assert "matches" in resp.json["search"]




# Fallo: Error en ejecución de consulta
@patch("utils.queries.Artist.search_artist.db.session.execute")
def test_ejecutar_busqueda_db_error(mock_execute, app):
    mock_execute.side_effect = Exception("DB error")

    text_mock = MagicMock()
    text_mock.name = "Radiohead"

    with app.app_context():
        resp, status = ejecutarBusquedaDB(text_mock)

    assert status == 500
    assert "error" in resp.json
