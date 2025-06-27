import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from utils.queries.Cluster.crear_cluster_genero import crearClusterGeneroData
from utils.queries.Cluster.get_clusters import getClusters
from utils.queries.Cluster.get_clusters_genero import getClusterGenero

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    return app

# ---------------- Test: crearClusterGeneroData válido ----------------
def test_crear_cluster_genero_data_valido():
    data = {
        "name": "Cluster A",
        "description": "Descripción del cluster",
        "is_active": True
    }

    cluster_obj, resp, status = crearClusterGeneroData(data)

    assert cluster_obj is not None
    assert cluster_obj.name == "Cluster A"
    assert resp is None
    assert status is None


# ---------------- Test: crearClusterGeneroData sin nombre ----------------
def test_crear_cluster_genero_data_sin_nombre():
    data = {
        "description": "Descripción sin nombre",
        "is_active": True
    }

    cluster_obj, resp, status = crearClusterGeneroData(data)

    assert cluster_obj is None
    assert status == 400
    assert "name" in resp["error"]


