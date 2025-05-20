import pytest
from unittest.mock import *
import json
from main import app
from configBd import *
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_db():
    with patch('psycopg2.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.__exit__.return_value = None
        mock_cur.__enter__.return_value = mock_cur
        mock_cur.__exit__.return_value = None
        yield mock_cur

@pytest.fixture
def authenticated_client(client):
    with client.session_transaction() as session:
        # Simula que el usuario está autenticado
        session['_user_id'] = '1'  # Flask-Login usa esta clave
    return client

def test_panel_rutas(authenticated_client):
    response = authenticated_client.get('/rutas')
    assert response.status_code == 200
    assert b'Rutas recomendadas' in response.data

def test_rutas_recomendadas_sin_login(client):
    response = client.get('/api/rutas_recomendadas', headers={'Accept': 'application/json'})
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert 'Usuario no autenticado' in data['message']