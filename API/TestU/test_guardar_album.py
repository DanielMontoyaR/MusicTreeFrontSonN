import pytest
from unittest.mock import patch, MagicMock
from flask import Flask

from utils.queries.Artist.guardar_album import guardar_album_individual



@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    return app

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



