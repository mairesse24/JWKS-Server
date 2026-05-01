import sqlite3
import os
import base64
from os import urandom

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

DB_FILE = "totally_not_my_privateKeys.db"


# =========================
# AES KEY
# =========================
def get_aes_key():
    key = os.getenv("NOT_MY_KEY")
    if not key:
        raise Exception("Missing NOT_MY_KEY environment variable")

    return key.encode().ljust(32)[:32]


# =========================
# ENCRYPT / DECRYPT
# =========================
def encrypt_key(pem_bytes):
    key = get_aes_key()
    iv = urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()

    encrypted = encryptor.update(pem_bytes) + encryptor.finalize()

    return (
        base64.b64encode(encrypted).decode("utf-8"),
        base64.b64encode(iv).decode("utf-8")
    )


def decrypt_key(enc_b64, iv_b64):
    key = get_aes_key()

    encrypted = base64.b64decode(enc_b64)
    iv = base64.b64decode(iv_b64)

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    decryptor = cipher.decryptor()

    return decryptor.update(encrypted) + decryptor.finalize()


# =========================
# INIT DB
# =========================
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS keys(
            kid INTEGER PRIMARY KEY AUTOINCREMENT,
            encrypted_key BLOB NOT NULL,
            iv BLOB NOT NULL,
            exp INTEGER NOT NULL
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            email TEXT UNIQUE,
            date_registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS auth_logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_ip TEXT NOT NULL,
            request_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)

        conn.commit()


# =========================
# SAVE KEY
# =========================
def save_key(pem_bytes, exp):
    encrypted, iv = encrypt_key(pem_bytes)

    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()

        c.execute(
            "INSERT INTO keys (encrypted_key, iv, exp) VALUES (?, ?, ?)",
            (encrypted, iv, exp)
        )

        conn.commit()


# =========================
# LOAD KEYS (FIXED)
# =========================
def load_keys():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT kid, encrypted_key, iv, exp FROM keys")
        rows = c.fetchall()

    keys = []

    for kid, enc, iv, exp in rows:
        try:
            pem = decrypt_key(enc, iv)

            private_key = serialization.load_pem_private_key(
                pem,
                password=None
            )

            keys.append({
                "kid": kid,
                "private_key": private_key,
                "public_key": private_key.public_key(),
                "exp": exp
            })

        except Exception:
            continue

    return keys


# =========================
# AUTH LOGGING
# =========================
def log_auth(ip, user_id):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()

        c.execute(
            "INSERT INTO auth_logs (request_ip, user_id) VALUES (?, ?)",
            (str(ip), user_id)
        )

        conn.commit()