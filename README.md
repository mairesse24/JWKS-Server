# JWKS Server Project

## Description
This project implements a **JWKS (JSON Web Key Set) server** that:

- Generates RSA key pairs with unique `kid`s and expiry timestamps
- Provides a **JWKS endpoint** (`/.well-known/jwks.json`) serving only unexpired public keys
- Implements an **/auth endpoint** that issues signed JWTs
  - Supports issuing expired JWTs via the `?expired=true` query parameter
- Demonstrates key expiry and proper `kid` usage in JWTs

This project is for educational purposes. In a production system, you would implement proper authentication and follow security best practices.

---

## Requirements
- Go (1.21+ recommended)
- Gin Web Framework
- Windows, macOS, or Linux terminal (PowerShell or bash)

---

## Installation / Setup

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/jwks-server.git
cd jwks-server
