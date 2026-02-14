# JWKS Server (FastAPI)

A simple JSON Web Key Set (JWKS) server built with FastAPI.

This project:  
- Generates RSA key pairs  
- Serves public keys via a JWKS endpoint  
- Issues signed JWTs  
- Supports expired key testing  
- Includes automated tests with coverage  

---

## 🚀 Features

- 🔐 RSA key generation  
- 🔁 Automatic key rotation (background thread)  
- 📦 JWKS endpoint (`/jwks.json`)  
- 🪪 JWT issuing endpoint (`/auth`)  
- 🧪 Pytest test suite  
- 📊 Code coverage reporting  

---

## 🛠 Installation

1. Clone or download the project.  
2. Create a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```
1. Clone the repository:

```bash
https://github.com/mairesse24/JWKS-Server
cd jwks-server

or python -m venv venv
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
- Only **unexpired keys** are included.  
- Each key has a **unique `kid`** that clients use to verify JWTs.  
- The JSON output includes key parameters like `kty` (key type), `alg` (algorithm), `n` (modulus), and `e` (exponent).
  
<p align="center">
  <img src="https://image2url.com/r2/default/images/1771042679290-138360e1-17e3-4fa3-89aa-c0dc23ee6fdb.png" width="500"/>
</p>


### POST /auth
Generates a signed JWT.
```bash
curl -X POST -H "Content-Type: application/json" -d '{"sub":"testuser"}' http://127.0.0.1:8080/auth
```

- Demonstrates that the server can issue a signed JWT.  
- The JWT includes a **header with `kid`**, so the client knows which key from the JWKS to use for verification.  
- Using the `?expired=true` query parameter issues a JWT signed with an **expired key**, useful for testing key rotation behavior.

<p align="center">
  <img src="https://image2url.com/r2/default/images/1771042504646-a60baa20-1ae2-435a-9652-5a2bf1316014.png" width="500"/>
</p>

## Running Tests
Run all tests:
```bash
python -m pytest
//Run tests with coverage:

python -m pytest --cov=.
//Generate HTML coverage report

python -m pytest --cov=. --cov-report=html
//HTML report will be in

htmlcov/index.html
```

## Coverage
Confirms that **all tests pass**.
Shows **coverage percentage** of **86%**  
- Ensures that your server functions correctly and all endpoints behave as expected.
<p align="center">
  <img src="https://image2url.com/r2/default/images/1771041863827-a31a7fb9-ec9d-4d35-9d02-f34945a8cef7.png" width="500"/>
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




------

# JWKS Server Project

## Description
This project implements a **JWKS (JSON Web Key Set) server** that:

- Generates RSA key pairs with unique `kid`s and expiry timestamps
- Provides a **JWKS endpoint** (`/.well-known/jwks.json`) serving only unexpired public keys
- Implements an **/auth endpoint** that issues signed JWTs
  - Supports issuing expired JWTs via the `?expired=true` query parameter
- Demonstrates key expiry and proper `kid` usage in JWTs


## Requirements
- Go (1.21+ recommended)
- Gin Web Framework
- Windows, macOS, or Linux terminal (PowerShell or bash)













