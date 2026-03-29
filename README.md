# JWKS Server Project

A JSON Web Key Set (JWKS) server demonstrating both in-memory key management and persistent database-backed key storage.

This repository contains two versions of the JWKS server:
Project 1 – FastAPI (In-Memory Keys)
Project 2 – Flask + SQLite (Persistent Keys)

This project:  
- Generates RSA key pairs  
- Serves public keys via a JWKS endpoint  
- Issues signed JWTs  
- Supports expired key testing  
- Includes automated tests with coverage  


## Features
- RSA key generation
- JWKS endpoint to serve public keys
- JWT issuing endpoint with kid headers
- Expired key support for testing key rotation
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
venv\Scripts\activate
```

### Install dependencies:
pip install -r requirements.txt


## Project 1 – FastAPI (In-Memory Keys)
Keys are generated and stored in memory
Endpoints:
- GET /jwks.json – returns active keys
- POST /auth – issues signed JWTs (add ?expired=true for expired key)
- Automatic key rotation in a background thread
- Pytest test suite with coverage (~86%)

### Running the Server
Start the server:
```bash
python -m uvicorn main:app --reload --port 8080
```
Server will run at:
```bash
http://127.0.0.1:8080
```

## Endpoints
### GET /jwks.json
Returns active public keys in JWKS format.
```bash
curl http://127.0.0.1:8080/jwks.json
```

- Only unexpired keys are included.
- Each key has a unique kid for verification.
- JSON output includes key parameters: kty (key type), alg (algorithm), n (modulus), and e (exponent).
  
<p align="center">
  <img src="https://i.postimg.cc/y8wZn9ds/jkws-endpoint.png" width="600; max-width: 900px;"/>
</p>

### POST /auth
Generates a signed JWT.
```bash
curl -X POST -H "Content-Type: application/json" -d '{"sub":"testuser"}' http://127.0.0.1:8080/auth
```

- Demonstrates issuing a signed JWT.
- JWT includes a header with kid for key verification.
- Add ?expired=true to issue a JWT signed with an expired key for testing rotation.
  
<p align="center">
  <img src="https://i.postimg.cc/8zq6wW5V/auth-endpoint.png" width="600; max-width: 900px;"/>
</p>

## Coverage 
- Confirms that all tests pass.
- Shows coverage percentage **(~86%)**.
- Ensures all endpoints function as expected.
<p align="center">
  <img src="https://i.postimg.cc/RZjHGfFv/coverage.png" width="600; max-width: 900px;"/>
</p>

## Project 2 – Flask + SQLite (Persistent Keys)
- Keys are stored in a SQLite database (keys table)
Endpoints:
- GET /.well-known/jwks.json – returns active keys from DB
- POST /auth – issues signed JWTs using DB keys
- Supports expired keys for testing

### Automated tests 
gradebot coverage with  ~96% coverage
<p align="center">
  <img src="https://postimg.cc/SJFjC3T6" width="600; max-width: 900px;"/>
</p>

### Run the server:
``` python main.py ```

### Inspect database keys:
```python view_keys.py ```


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

## | Feature             | Project 1 (FastAPI) | Project 2 (Flask + SQLite) |
| ------------------- | ------------------- | -------------------------- |
| Key Storage         | In-memory           | SQLite DB                  |
| Key Persistence     | No                  | Yes                        |
| Framework           | FastAPI             | Flask                      |
| JWT Issuing         | Yes                 | Yes                        |
| Expired Key Support | Yes                 | Yes                        |
| Tests & Coverage    | ~86%                | ~96%                       |
| Database Queries    | N/A                 | Parameterized, secure      |


## Technologies Used
-  FastAPI (Project 1)
-  Flask (Project 2)
-  Uvicorn
-  PyJWT
-  Cryptography
-  SQLite (Project 2)
-  Pytest, Pytest-Cov

## Notes
-  Expired keys are intentionally supported for testing.
-  Active keys are returned in the JWKS endpoint.
-  All keys are stored in memory.
