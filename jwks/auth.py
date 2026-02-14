# auth.py
from datetime import datetime, timedelta
from jose import jwt
from keys import keys
from cryptography.hazmat.primitives import serialization

JWT_ISSUER = "my-jwks-server"
JWT_AUDIENCE = "my-audience"
JWT_ALGORITHM = "RS256"

def create_jwt(sub: str, expired: bool = False):
    now = datetime.utcnow()
    if expired:
        key_data = next((k for k in keys.values() if k.expiry < now), None)
        if not key_data:
            raise RuntimeError("No expired keys available")
    else:
        key_data = next((k for k in keys.values() if k.expiry > now), None)
        if not key_data:
            raise RuntimeError("No active keys available")

    private_pem = key_data.private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    payload = {
        "sub": sub,
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=30)).timestamp())
    }

    token = jwt.encode(payload, private_pem, algorithm=JWT_ALGORITHM, headers={"kid": key_data.kid})
    return {"token": token, "kid": key_data.kid, "expiry": key_data.expiry.isoformat()}
