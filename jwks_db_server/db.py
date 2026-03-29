# db.py
"""
Database module for managing RSA keys in SQLite.
"""

import sqlite3
import time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

DB_FILE = "totally_not_my_privateKeys.db"

def init_db():
    """Create the keys table if it does not exist."""
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS keys(
                kid INTEGER PRIMARY KEY AUTOINCREMENT,
                key BLOB NOT NULL,
                exp INTEGER NOT NULL
            )
        ''')
        conn.commit()


def save_key(pem_bytes: bytes, expiry: int):
    """Save a PEM-encoded private key with expiry timestamp."""
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO keys (key, exp) VALUES (?, ?)', (pem_bytes, expiry))
        conn.commit()


def load_keys():
    """Load all keys from the database and return as a list of dicts."""
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('SELECT kid, key, exp FROM keys')
        rows = c.fetchall()

    keys = []
    for kid, key_blob, exp in rows:
        private_key = serialization.load_pem_private_key(
            key_blob, password=None, backend=default_backend()
        )
        public_key = private_key.public_key()
        keys.append({'kid': kid, 'private_key': private_key, 'public_key': public_key, 'exp': exp})
    return keys