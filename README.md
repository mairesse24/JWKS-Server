# JWKS Server 
A JSON Web Key Set (JWKS) server demonstrating both in-memory key management and persistent database-backed key storage.  
This repository contains two versions of the JWKS server:

## Project 1: Basic JWKS Server
- RESTful server serving public keys in JWKS format
- Issues JWTs signed with valid or expired keys
- Keys are stored in memory (non-persistent)
- Directory: [jwks](./jwks)
- Test coverage: ~86%

## Project 2: SQLite-backed JWKS Server
- Extends Project 1 by storing private keys in a SQLite database
- Securely signs JWTs and exposes JWKS endpoint
- Parameterized queries to prevent SQL injection
- Directory: [jwks_db_server](./jwks_db_server)
- Test coverage: ~96%

## Project 3: Secure JWKS Server (Encrypted SQLite + Hardened Auth System)
- Extends Project 2 by adding AES-encrypted RSA private key storage
- Implements secure key encryption using AES-256 (CFB mode)
- Adds robust JWT authentication with key rotation support
- Improves database integrity and logging consistency
- Fixes edge cases in key loading by safely handling corrupted keys
- Maintains SQLite persistence with improved security model
- Directory: [jwks_auth_service](./jwks_auth_service)
- Test coverage: ~74%–

## Features  
### Core Features (All Projects)
- RSA key pair generation
- JWKS endpoint to serve active public keys
- JWT issuing endpoint with kid headers
- Support for expired keys for testing key rotation
- Automated tests with coverage reporting
### Project 2 (SQLite Persistence)
- SQLite-backed key storage
- Parameterized queries to prevent SQL injection
- Persistent user and key data
- Database-backed authentication logging
### Project 3 (Security Enhancements)
- AES-256 encryption of private RSA keys before database storage
- Secure IV generation per key
- Base64-safe encoding for database compatibility
- RS256 (RSA SHA-256) JWT signing
- Authentication request logging with user tracking
- Rate limiting on /auth endpoint
- Graceful handling of corrupted or invalid keys
- Environment-based encryption key (NOT_MY_KEY)

## Installation
1. Clone the repository:
```bash
git clone https://github.com/mairesse24/JWKS-Server
cd jwks
```
2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate   # Windows
# or
source venv/bin/activate  # macOS/Linux
```

### Install dependencies:
pip install -r requirements.txt

---

## Project 1 – FastAPI (In-Memory Keys)
Keys are generated and stored in memory
Endpoints:
- GET /jwks.json – returns active public keys
- POST /auth – issues signed JWTs
- Use ?expired=true to issue a JWT signed with an expired key

### Running the Server
Start the server:
```bash
python -m uvicorn main:app --reload --port 8080
```
Server URL:
```bash
http://127.0.0.1:8080
```
### Example Usage
 
Get active keys
```bash
curl http://127.0.0.1:8080/jwks.json
```
<p align="center">
  <img src="https://i.postimg.cc/y8wZn9ds/jkws-endpoint.png" width="600; max-width: 900px;"/>
</p>

Issue JWT
```bash
curl -X POST -H "Content-Type: application/json" -d '{"sub":"testuser"}' http://127.0.0.1:8080/auth
```
<p align="center">
  <img src="https://i.postimg.cc/8zq6wW5V/auth-endpoint.png" width="600; max-width: 900px;"/>
</p>

Issue JWT with expired key
```bash
curl -X POST http://127.0.0.1:8080/auth?expired=true
```

### Test Coverage 
<p align="center">
  <img src="https://i.postimg.cc/RZjHGfFv/coverage.png" width="600; max-width: 900px;"/>
</p>

---

## Project 2 – Flask + SQLite (Persistent Keys)
Keys are stored in a SQLite database (`totally_not_my_privateKeys.db`)  
Endpoints:
- GET /.well-known/jwks.json – returns active keys from DB
- POST /auth – issues signed JWTs using DB keys
- Supports expired keys for testing

### Run the server:
```bash
python main.py
```
### Inspect database keys:
```bash
python view_keys.py
```
This ensures at least one expired and one valid key exists for testing.

### Automated tests 
Gradebot test client shows ~96% coverage.
<p align="center">
  <img src="https://i.postimg.cc/SNj8Fpcv/gradebot.png" width="600; max-width: 900px;"/>
</p>

Test coverage screenshot shows 76% coverage of the test suite:
<p align="center">
  <img src="https://i.postimg.cc/7bv7mVq8/Screenshot-2026-03-29-152324.png" width="600; max-width: 900px;"/>
</p>

---

## Security Improvements (Project 3)
Private keys are never stored in plaintext
Encryption keys sourced from environment variable:
```bash
NOT_MY_KEY
```
Prevents database leakage from exposing usable private keys
Skips malformed keys instead of crashing server/tests

### Coverage report 
Gradebot test client shows ~74% coverage.
<p align="center">
  <img src="https://i.postimg.cc/FRp7QsJz/Screenshot-2026-05-01-105226.png" width="600; max-width: 900px;"/>
</p>

Test coverage screenshot shows 74% coverage of the test suite:
<p align="center">
  <img src="https://i.postimg.cc/SNBQ3zt2/Screenshot-2026-05-01-110332.png" width="600; max-width: 900px;"/>
</p>


### Run the server:
```bash
python main.py
```
### Register user
```bash
Invoke-RestMethod -Method POST `
  -Uri "http://127.0.0.1:8080/register" `
  -ContentType "application/json" `
  -Body '{"username":"test","email":"test@test.com"}'
```
---

## Running Tests
Run all tests:
```bash
python -m pytest
```
Run tests with coverage:
```bash
python -m pytest --cov=.
```
Generate HTML coverage report:
```bash
python -m pytest --cov=. --cov-report=html
```
The HTML report will be generated in:
```bash
htmlcov/index.html
```


## Technologies Used
- FastAPI (Project 1)
- Flask (Project 2 & 3)
- SQLite
- PyJWT
- Cryptography (AES + RSA)
- Uvicorn
- Pytest, Pytest-Cov
- Argon2 (password hashing)


## Feature Comparison

| Feature              | Project 1 (FastAPI) | Project 2 (Flask + SQLite) | Project 3 (Secure SQLite) |
| -------------------- | ------------------- | -------------------------- | ------------------------- |
| Key Storage          | In-memory           | SQLite DB                  | SQLite DB                 |
| Key Persistence      | No                  | Yes                        | Yes                       |
| Private Key Security | None                | None                       | AES-256 encrypted         |
| Framework            | FastAPI             | Flask                      | Flask                     |
| JWT Issuing          | Yes                 | Yes                        | Yes                       |
| Signing Algorithm    | RS256               | RS256                      | RS256                     |
| Expired Key Support  | Yes                 | Yes                        | Yes                       |
| Auth Logging         | No                  | Yes                        | Yes                       |
| Rate Limiting        | No                  | Basic                      | Yes                       |
| Tests & Coverage     | ~86%                | ~96%                       | ~74%                      |
| Database Queries     | N/A                 | Parameterized, secure      | Parameterized, secure     |
---

## Notes
- Expired keys are intentionally supported for testing
- Active keys are returned in the JWKS endpoint
- Private keys are encrypted using AES-256 before being stored in SQLite
- Keys are decrypted only at runtime for signing operations
- Corrupted keys are skipped to maintain service stability
- NOT_MY_KEY environment variable is required for encryption/decryption
