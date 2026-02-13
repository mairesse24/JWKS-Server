package main

import (
	"crypto/rand"
	"crypto/rsa"
	"encoding/base64"
	"math/big"
	"time"

	"github.com/google/uuid"
)

var keys []Key

func generateKey(expiry time.Duration) Key {
	privateKey, _ := rsa.GenerateKey(rand.Reader, 2048)

	k := Key{
		KID:       uuid.NewString(),
		Private:   privateKey,
		Public:    &privateKey.PublicKey,
		ExpiresAt: time.Now().Add(expiry),
	}

	return k
}

func initKeys() {
	// Valid key
	validKey := generateKey(1 * time.Hour)

	// Expired key
	expiredKey := generateKey(-1 * time.Hour)

	keys = []Key{validKey, expiredKey}
}

func rsaPublicKeyToJWK(key Key) map[string]interface{} {
	n := base64.RawURLEncoding.EncodeToString(key.Public.N.Bytes())
	e := base64.RawURLEncoding.EncodeToString(big.NewInt(int64(key.Public.E)).Bytes())

	return map[string]interface{}{
		"kty": "RSA",
		"use": "sig",
		"alg": "RS256",
		"kid": key.KID,
		"n":   n,
		"e":   e,
	}
}
