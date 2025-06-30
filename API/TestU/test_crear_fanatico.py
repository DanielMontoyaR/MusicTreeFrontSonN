import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from utils.queries.Fanatico.crear_fanatico import crearFanatico
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    return app

# ---------------- Test: crearFanatico válido ----------------
def test_crear_fanatico_valido(app):
    data = {
        "username": "fan123",
        "password": "contrasena_segura",
        "fullname": "Juan Pérez",
        "country": "México",
        "avatar": "3",
        "favorite_genres": ["1", "2"]
    }

    with app.app_context():
        fan, resp, status = crearFanatico(data)

    assert fan is not None
    assert fan["username"] == "fan123"
    assert resp is None
    assert status is None