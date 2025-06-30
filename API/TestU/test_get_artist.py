import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from utils.queries.Artist.get_artists import getArtists



@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    return app

# ---------------- TEST: getArtists mockeando query SQL ----------------
@patch("utils.queries.Artist.get_artists.db.session.execute")
def test_get_artists(mock_execute, app):
    mock_execute.return_value = [MagicMock(_mapping={"name": "Radiohead"})]

    with app.app_context():
        resp = getArtists()

    assert isinstance(resp.json, list)
    assert resp.json[0]["name"] == "Radiohead"

# Fallo: Error en ejecución SQL
@patch("utils.queries.Artist.get_artists.db.session.execute")
def test_get_artists_error(mock_execute, app):
    mock_execute.side_effect = Exception("DB error")

    with app.app_context():
        resp, status = getArtists()

    assert status == 500
    assert "error" in resp.json


