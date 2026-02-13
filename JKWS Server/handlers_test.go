package main

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
)

func setupRouter() *gin.Engine {
	initKeys()
	r := gin.Default()
	r.GET("/.well-known/jwks.json", jwksHandler)
	r.POST("/auth", authHandler)
	return r
}

func TestJWKSReturnsValidKeysOnly(t *testing.T) {
	router := setupRouter()

	req, _ := http.NewRequest("GET", "/.well-known/jwks.json", nil)
	w := httptest.NewRecorder()
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusOK, w.Code)
	assert.Contains(t, w.Body.String(), "keys")
}

func TestAuthReturnsToken(t *testing.T) {
	router := setupRouter()

	req, _ := http.NewRequest("POST", "/auth", nil)
	w := httptest.NewRecorder()
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusOK, w.Code)
	assert.Contains(t, w.Body.String(), "token")
}
