# JWKS Server Project

A simple JSON Web Key Set (JWKS) server built with FastAPI.

This project:  
- Generates RSA key pairs  
- Serves public keys via a JWKS endpoint  
- Issues signed JWTs  
- Supports expired key testing  
- Includes automated tests with coverage  

---

## Features

- RSA key generation  
- Automatic key rotation (background thread)  
- JWKS endpoint (`/jwks.json`)  
- JWT issuing endpoint (`/auth`)  
- Pytest test suite  
- Code coverage reporting  

---

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
pip install fastapi uvicorn cryptography pyjwt pytest pytest-cov

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

## Coverage
- Confirms that all tests pass.
- Shows coverage percentage **(~86%)**.
- Ensures all endpoints function as expected.
<p align="center">
  <img src="https://i.postimg.cc/RZjHGfFv/coverage.png" width="600; max-width: 900px;"/>
</p>

## Technologies Used
-  FastAPI
-  Uvicorn
-  PyJWT
-  Cryptography
-  Pytest
-  Pytest-Cov

## Notes
-  Expired keys are intentionally supported for testing.
-  Active keys are returned in the JWKS endpoint.
-  All keys are stored in memory.
