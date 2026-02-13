package main

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
)

func TestJWKSReturnsOnlyValidKeys(t *testing.T) {
	gin.SetMode(gin.TestMode)

	initKeys()
	router := gin.Default()
	router.GET("/.well-known/jwks.json", jwksHandler)

	req, _ := http.NewRequest("GET", "/.well-known/jwks.json", nil)
	w := httptest.NewRecorder()
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusOK, w.Code)

	var response JWKS
	err := json.Unmarshal(w.Body.Bytes(), &response)
	assert.Nil(t, err)

	// Should only return unexpired keys
	for _, key := range response.Keys {
		assert.NotEmpty(t, key["kid"])
		assert.Equal(t, "RSA", key["kty"])
		assert.Equal(t, "RS256", key["alg"])
		assert.NotEmpty(t, key["n"])
		assert.NotEmpty(t, key["e"])
	}

	// Ensure none of the returned keys are expired
	for _, storedKey := range keys {
		if time.Now().After(storedKey.ExpiresAt) {
			for _, returnedKey := range response.Keys {
				assert.NotEqual(t, storedKey.KID, returnedKey["kid"])
			}
		}
	}
}
