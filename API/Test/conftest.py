import pytest
import sys
import os

# Agrega la raíz al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from API.api import app  # ← Importa como módulo

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
