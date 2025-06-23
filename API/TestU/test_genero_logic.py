import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from utils.queries.Genre.crear_genero import crearGeneroData, validar_genero
from utils.queries.Genre.get_generos import getGeneros
from utils.queries.Genre.get_subgeneros import getSubGeneros
from utils.queries.Genre.importjsongenre import procesar_generos_batch

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    return app


# ---------------- Test: validar_genero con padre inexistente ----------------
@patch("utils.queries.Genre.crear_genero.db.session.get")
def test_validar_genero_padre_inexistente(mock_get, app):
    mock_get.return_value = None
    data = {"name": "Hardstyle", "is_subgenre": True, "parent_genre_id": 999}

    with app.app_context():
        _, resp, status = validar_genero(data)

    assert status == 400
    assert "no existe" in resp.json["error"]


# ---------------- Test: crearGeneroData con datos válidos ----------------
@patch("utils.queries.Genre.crear_genero.db.session.get")
def test_crear_genero_data_exitoso(mock_get, app):
    mock_get.return_value = MagicMock()
    data = {
        "name": "Techno", "description": "Género", "is_active": True,
        "color": "#FF0000", "creation_year": "1990", "country_of_origin": "Germany",
        "average_mode": "5", "bpm_lower": "120", "bpm_upper": "140",
        "dominant_key": "C", "typical_volume": "0.8", "time_signature": "4/4",
        "average_duration": "240", "is_subgenre": False, "cluster_id": 1
    }

    with app.app_context():
        genero_obj, resp, status = crearGeneroData(data)

    assert genero_obj is not None
    assert genero_obj.name == "Techno"
    assert resp is None
    assert status is None




# ---------------- Test: procesar_generos_batch con errores y éxito ----------------
@patch("utils.queries.Genre.importjsongenre.guardarGeneroDB")
@patch("utils.queries.Genre.importjsongenre.crearGeneroData")
def test_procesar_generos_batch(mock_crear, mock_guardar, tmp_path, app):
    # Simula un género válido y uno con error
    genero_valido = {"name": "Techno", "is_subgenre": False}
    genero_invalido = {"name": "", "is_subgenre": False}

    mock_crear.side_effect = [
        (MagicMock(), None, None),  # OK
        (None, MagicMock(get_data=lambda as_text: '{"error": "Faltan datos"}'), 400)  # Error
    ]
    mock_guardar.return_value = (MagicMock(get_data=lambda as_text: "{}"), 200)

    generos = [genero_valido, genero_invalido]

    with app.app_context():
        result, _, status = procesar_generos_batch(generos, carpeta_destino=str(tmp_path))

    assert status == 200
    assert "errores" in result
    assert len(result["errores"]) == 1
    assert result["errores"][0]["index"] == 1
    assert "Faltan datos" in result["errores"][0]["error"]
