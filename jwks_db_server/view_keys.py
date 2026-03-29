# view_keys.py
import sqlite3
import time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os

# Use a relative path for portability
DB_FILE = os.path.join(os.path.dirname(__file__), "totally_not_my_privateKeys.db")

def main():
    """Connect to the SQLite DB and display all RSA keys with expiry status."""
    
    # Connect to the database using context manager
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        
        # Use parameterized query with real logic for filtering (all keys)
        current_time = int(time.time())
        query = "SELECT kid, key, exp FROM keys"
        c.execute(query)  # no user input needed, so parameters not strictly required
        
        # Fetch and display each key
        for kid, key_blob, exp in c.fetchall():
            # Load the private key from the BLOB
            private_key = serialization.load_pem_private_key(
                key_blob, password=None, backend=default_backend()
            )
            # Convert private key back to PEM format for display
            pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            status = "valid" if exp > current_time else "expired"
            
            print(f"Key ID: {kid}, Expiry: {exp} ({status})\n{pem.decode()}\n{'-'*60}")

if __name__ == "__main__":
    main()