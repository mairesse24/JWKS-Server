# keys.py
from datetime import datetime, timedelta
from typing import Dict
import uuid
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from base64 import urlsafe_b64encode

# ===== DATA STRUCTURES =====
class KeyData:
    def __init__(self, private_key, public_key, kid, expiry):
        self.private_key = private_key
        self.public_key = public_key
        self.kid = kid
        self.expiry = expiry

# In-memory key storage
keys: Dict[str, KeyData] = {}

# ===== KEY GENERATION =====
def generate_rsa_keypair(expired=False) -> KeyData:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    kid = str(uuid.uuid4())
    expiry = datetime.utcnow() + timedelta(seconds=60)  # 1 minute
    if expired:
        expiry = datetime.utcnow() - timedelta(seconds=10)

    key_data = KeyData(private_key, public_key, kid, expiry)
    keys[kid] = key_data
    return key_data

# ===== JWKS FORMAT =====
def public_key_to_jwk(key_data: KeyData) -> Dict:
    public_numbers = key_data.public_key.public_numbers()
    e = public_numbers.e.to_bytes((public_numbers.e.bit_length() + 7) // 8, "big")
    n = public_numbers.n.to_bytes((public_numbers.n.bit_length() + 7) // 8, "big")

    def b64u(data: bytes) -> str:
        return urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")

    return {
        "kty": "RSA",
        "use": "sig",
        "kid": key_data.kid,
        "alg": "RS256",
        "n": b64u(n),
        "e": b64u(e)
    }

# ===== KEY ROTATION =====
def rotate_keys():
    import time
    while True:
        now = datetime.utcnow()
        expired_kids = [kid for kid, k in keys.items() if k.expiry < now - timedelta(seconds=60)]
        for kid in expired_kids:
            del keys[kid]

        if not any(k.expiry > now for k in keys.values()):
            generate_rsa_keypair()
        time.sleep(10)
