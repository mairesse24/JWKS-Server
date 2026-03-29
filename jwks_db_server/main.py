# main.py
from flask import Flask, jsonify, request
import time
import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from base64 import urlsafe_b64encode
import os
from db import init_db, save_key, load_keys

app = Flask(__name__)

def generate_key(expired=False):
    """
    Generate an RSA private key, serialize to PEM, and store in DB.
    
    Args:
        expired (bool): Whether the key should already be expired.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    expiry = int(time.time() + 3600)  # 1 hour from now
    if expired:
        expiry = int(time.time() - 3600)  # already expired

    save_key(pem, expiry)


@app.route('/.well-known/jwks.json', methods=['GET'])
def jwks():
    """Return all non-expired public keys in JWKS format."""
    current_time = int(time.time())
    jwks_keys = []

    for key_data in load_keys():
        if key_data['exp'] > current_time:
            n_int = key_data['public_key'].public_numbers().n
            e_int = key_data['public_key'].public_numbers().e
            n_b64 = urlsafe_b64encode(n_int.to_bytes((n_int.bit_length()+7)//8, 'big')).rstrip(b'=').decode('utf-8')
            e_b64 = urlsafe_b64encode(e_int.to_bytes((e_int.bit_length()+7)//8, 'big')).rstrip(b'=').decode('utf-8')
            jwks_keys.append({
                'kty': 'RSA',
                'kid': str(key_data['kid']),
                'use': 'sig',
                'alg': 'RS256',
                'n': n_b64,
                'e': e_b64
            })

    return jsonify({'keys': jwks_keys})


@app.route('/auth', methods=['POST'])
def auth():
    """Return a JWT signed with a valid or expired key based on query parameter."""
    expired = request.args.get('expired', 'false').lower() == 'true'
    current_time = int(time.time())
    keys_list = load_keys()

    selected = None
    for key_data in keys_list:
        if expired and key_data['exp'] < current_time:
            selected = key_data
            break
        elif not expired and key_data['exp'] > current_time:
            selected = key_data
            break

    if not selected:
        return jsonify({"msg": "No valid keys"}), 404

    payload = {
        'sub': 'user',
        'iat': current_time,
        'exp': current_time + 300 if not expired else current_time - 30
    }
    token = jwt.encode(
        payload,
        selected['private_key'],
        algorithm='RS256',
        headers={'kid': str(selected['kid'])}
    )
    return jsonify(token=token)


if __name__ == '__main__':
    init_db()
    
    # Only generate keys if DB is empty
    if len(load_keys()) == 0:
        generate_key(expired=False)  # valid
        generate_key(expired=True)   # expired

    app.run(host='127.0.0.1', port=8080)