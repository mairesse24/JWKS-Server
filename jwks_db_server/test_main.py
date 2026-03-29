import pytest
from main import app, init_db, generate_key
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_jwks_endpoint(client):
    init_db()
    generate_key(expired=False)
    rv = client.get('/.well-known/jwks.json')
    data = rv.get_json()
    assert 'keys' in data
    assert len(data['keys']) > 0

def test_auth_endpoint(client):
    rv = client.post('/auth')
    data = rv.get_json()
    assert 'token' in data