package main

import (
	"crypto/rsa"
	"time"
)

type Key struct {
	KID       string
	Private   *rsa.PrivateKey
	Public    *rsa.PublicKey
	ExpiresAt time.Time
}

type JWKS struct {
	Keys []map[string]interface{} `json:"keys"`
}
