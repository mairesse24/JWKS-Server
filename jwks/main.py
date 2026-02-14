from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
import threading

from keys import generate_rsa_keypair, rotate_keys, keys, public_key_to_jwk
from auth import create_jwt

app = FastAPI(title="JWKS Server")

# 👇 ADD THIS LINE
app.keys = keys


# ===== STARTUP =====
@app.on_event("startup")
def startup_event():
    generate_rsa_keypair()
    generate_rsa_keypair(expired=True)
    threading.Thread(target=rotate_keys, daemon=True).start()


# ===== ROUTES =====
@app.get("/jwks.json")
def get_jwks():
    now = datetime.utcnow()
    active_keys = [
        public_key_to_jwk(k)
        for k in keys.values()
        if k.expiry > now
    ]
    return JSONResponse(content={"keys": active_keys})


class AuthRequest(BaseModel):
    sub: str


@app.post("/auth")
def auth(req: AuthRequest, expired: bool = Query(False)):
    try:
        return create_jwt(req.sub, expired)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
