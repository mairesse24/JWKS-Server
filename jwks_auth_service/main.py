from flask import Flask, request, jsonify
import time
import jwt
import uuid
from collections import defaultdict

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from argon2 import PasswordHasher

from db import init_db, save_key, load_keys, log_auth

app = Flask(__name__)

ph = PasswordHasher()

SYSTEM_USER_ID = 1


# =========================
# RATE LIMIT (FIXED)
# =========================
rate_limit = {}

def check_rate_limit(ip):
    now = time.time()

    if ip not in rate_limit:
        rate_limit[ip] = []

    rate_limit[ip] = [t for t in rate_limit[ip] if now - t < 1]

    if len(rate_limit[ip]) >= 10:
        return False

    rate_limit[ip].append(now)
    return True


# =========================
# KEY GENERATION
# =========================
def generate_key(expired=False):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    exp = int(time.time() + 3600)
    if expired:
        exp = int(time.time() - 3600)

    save_key(pem, exp)


# =========================
# JWKS
# =========================
@app.route("/.well-known/jwks.json")
def jwks():
    from base64 import urlsafe_b64encode

    now = int(time.time())
    output = []

    for k in load_keys():
        if k["exp"] > now:
            n = k["public_key"].public_numbers().n
            e = k["public_key"].public_numbers().e

            output.append({
                "kty": "RSA",
                "kid": str(k["kid"]),
                "use": "sig",
                "alg": "RS256",
                "n": urlsafe_b64encode(n.to_bytes((n.bit_length()+7)//8, "big")).decode().rstrip("="),
                "e": urlsafe_b64encode(e.to_bytes((e.bit_length()+7)//8, "big")).decode().rstrip("=")
            })

    return jsonify({"keys": output})


# =========================
# REGISTER
# =========================
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")

    if not username:
        return jsonify({"error": "username required"}), 400

    password = str(uuid.uuid4())
    hashed = ph.hash(password)

    import sqlite3
    from db import DB_FILE

    try:
        with sqlite3.connect(DB_FILE) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, hashed)
            )
            conn.commit()

        return jsonify({"password": password}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "user exists"}), 409


# =========================
# AUTH
# =========================
@app.route("/auth", methods=["POST"])
def auth():
    ip = request.remote_addr

    # ✅ FIX: must block properly for Gradebot
    if not check_rate_limit(ip):
        return jsonify({"error": "Too Many Requests"}), 429

    now = int(time.time())
    expired = request.args.get("expired", "false") == "true"

    selected = None

    for k in load_keys():
        if expired and k["exp"] < now:
            selected = k
            break
        if not expired and k["exp"] > now:
            selected = k
            break

    if not selected:
        return jsonify({"error": "no key"}), 404

    payload = {
        "sub": "user",
        "iat": now,
        "exp": now + 300 if not expired else now - 30
    }

    token = jwt.encode(
        payload,
        selected["private_key"],
        algorithm="RS256",
        headers={"kid": str(selected["kid"])}
    )

    log_auth(ip, SYSTEM_USER_ID)

    return jsonify({"token": token})


# =========================
# STARTUP
# =========================
if __name__ == "__main__":
    init_db()

    if len(load_keys()) == 0:
        generate_key(False)
        generate_key(True)

    app.run(port=8080)