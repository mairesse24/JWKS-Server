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

## Features  
- RSA key pair generation
- JWKS endpoint to serve active public keys
- JWT issuing endpoint with kid headers
- Support for expired keys for testing key rotation
- SQLite-backed key persistence (Project 2)
- Automated tests with coverage reporting

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

## Project 2 – Flask + SQLite (Persistent Keys)
Keys are stored in a SQLite database (`totally_not_my_privateKeys.db`)  
Endpoints:
- GET /.well-known/jwks.json – returns active keys from DB
- POST /auth – issues signed JWTs using DB keys
- Supports expired keys for testing

### Automated tests 
Gradebot test client shows ~96% coverage.
<p align="center">
  <img src="https://i.postimg.cc/SNj8Fpcv/gradebot.png" width="600; max-width: 900px;"/>
</p>

### Run the server:
```bash
python main.py
```

### Inspect database keys:
```bash
python view_keys.py ```

This ensures at least one expired and one valid key exists for testing.


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
-  FastAPI (Project 1)
-  Flask (Project 2)
-  Uvicorn
-  PyJWT
-  Cryptography
-  SQLite (Project 2)
-  Pytest, Pytest-Cov

## Feature Comparison

| Feature                  | Project 1 (FastAPI) | Project 2 (Flask + SQLite) |
| ------------------------ | ----------------- | -------------------------- |
| Key Storage               | In-memory         | SQLite DB                  |
| Key Persistence           | No                | Yes                        |
| Framework                 | FastAPI           | Flask                      |
| JWT Issuing               | Yes               | Yes                        |
| Expired Key Support       | Yes               | Yes                        |
| Tests & Coverage          | ~86%              | ~96%                       |
| Database Queries          | N/A               | Parameterized, secure      |

---

## Notes
-  Expired keys are intentionally supported for testing.
-  Active keys are returned in the JWKS endpoint.- 
- All keys are stored in memory (Project 1) or in SQLite DB (Project 2).
