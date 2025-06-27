import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from utils.queries.Fanatico.crear_fanatico import crearFanatico
from utils.queries.Fanatico.filtrar_artistas import buscarArtistasFiltrados
from utils.queries.Fanatico.login_fan import loginFanData
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


# ---------------- Test: buscarArtistasFiltrados con datos válidos ----------------
@patch("utils.queries.Fanatico.filtrar_artistas.db.session.execute")
def test_buscar_artistas_filtrados(mock_execute, app):
    mock_execute.return_value = [MagicMock(_mapping={"name": "Radiohead"})]

    data = {
        "genre_id": "1",
        "subgenre_id": "2",
        "nombre": "Radio",
        "limite": 10
    }

    with app.app_context():
        resultados, resp, status = buscarArtistasFiltrados(data)

    assert isinstance(resultados, list)
    assert resultados[0]["name"] == "Radiohead"
    assert resp is None
    assert status is None


# ---------------- Test: loginFanData con credenciales válidas ----------------
@patch("utils.queries.Fanatico.login_fan.db.session.execute")
def test_login_fan_valido(mock_execute, app):
    mock_row = (
        "fan-id-123", "Juan Pérez", "México", "avatar_3.png", "Autenticación exitosa"
    )
    mock_result = MagicMock()
    mock_result.fetchone.return_value = mock_row
    mock_execute.return_value = mock_result

    data = {
        "username": "fan123",
        "password": "contrasena_segura"
    }

    with app.app_context():
        resultado, resp, status = loginFanData(data)

    assert resultado is not None
    assert resultado["authenticated"] is True
    assert resultado["fan"]["full_name"] == "Juan Pérez"
    assert resp is None
    assert status is None


# ---------------- Test: loginFanData con contraseña incorrecta ----------------
@patch("utils.queries.Fanatico.login_fan.db.session.execute")
def test_login_fan_contrasena_incorrecta(mock_execute, app):
    mock_row = (
        None, None, None, None, "Contraseña incorrecta"
    )
    mock_result = MagicMock()
    mock_result.fetchone.return_value = mock_row
    mock_execute.return_value = mock_result

    data = {
        "username": "fan123",
        "password": "mala"
    }

    with app.app_context():
        resultado, resp, status = loginFanData(data)

    assert resultado is None
    assert resp.json["error"] == "Contraseña incorrecta"
    assert status == 401


# ---------------- Test: loginFanData con usuario inexistente ----------------
@patch("utils.queries.Fanatico.login_fan.db.session.execute")
def test_login_fan_usuario_inexistente(mock_execute, app):
    mock_result = MagicMock()
    mock_result.fetchone.return_value = None
    mock_execute.return_value = mock_result

    data = {
        "username": "usuario_falso",
        "password": "cualquiera"
    }

    with app.app_context():
        resultado, resp, status = loginFanData(data)

    assert resultado is None
    assert resp.json["authenticated"] is False
    assert status == 401
