from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

from keys import generate_rsa_keypair
from datetime import datetime, timedelta

client = TestClient(app)

# ===== Setup before tests =====
def setup_module(module):
    """Ensure at least one active and one expired key exist before tests."""
    now = datetime.utcnow()
    active_keys = [k for k in app.keys.values() if k.expiry > now]
    expired_keys = [k for k in app.keys.values() if k.expiry < now]

    if not active_keys:
        generate_rsa_keypair(expired=False)
    if not expired_keys:
        generate_rsa_keypair(expired=True)


# ===== TESTS =====
def test_jwks_returns_active_keys():
    r = client.get("/jwks.json")
    assert r.status_code == 200
    data = r.json()
    assert "keys" in data
    assert all("kid" in k for k in data["keys"])


def test_auth_returns_jwt():
    r = client.post("/auth", json={"sub": "testuser"})
    assert r.status_code == 200
    data = r.json()
    assert "token" in data
    assert "kid" in data


def test_auth_expired_key():
    r = client.post("/auth?expired=true", json={"sub": "testuser"})
    assert r.status_code == 200
    data = r.json()
    assert "token" in data
