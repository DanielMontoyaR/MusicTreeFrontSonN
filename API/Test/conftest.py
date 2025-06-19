import pytest
from api import app  # si hiciste el paso 3 o estás en PYTHONPATH

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
