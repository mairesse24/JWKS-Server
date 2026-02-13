package main

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
)

func jwksHandler(c *gin.Context) {
	var jwks JWKS

	for _, key := range keys {
		if time.Now().Before(key.ExpiresAt) {
			jwks.Keys = append(jwks.Keys, rsaPublicKeyToJWK(key))
		}
	}

	c.JSON(http.StatusOK, jwks)
}

func authHandler(c *gin.Context) {
	useExpired := c.Query("expired") != ""

	var selectedKey Key

	for _, key := range keys {
		if useExpired {
			if time.Now().After(key.ExpiresAt) {
				selectedKey = key
			}
		} else {
			if time.Now().Before(key.ExpiresAt) {
				selectedKey = key
			}
		}
	}

	token := jwt.NewWithClaims(jwt.SigningMethodRS256, jwt.MapClaims{
		"sub": "fakeUser",
		"exp": selectedKey.ExpiresAt.Unix(),
		"iat": time.Now().Unix(),
	})

	token.Header["kid"] = selectedKey.KID

	signedToken, _ := token.SignedString(selectedKey.Private)

	c.JSON(http.StatusOK, gin.H{
		"token": signedToken,
	})
}
