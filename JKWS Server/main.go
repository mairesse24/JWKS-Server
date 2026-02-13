package main

import "github.com/gin-gonic/gin"

func main() {
	initKeys()

	r := gin.Default()

	r.GET("/.well-known/jwks.json", jwksHandler)
	r.POST("/auth", authHandler)

	r.Run(":8080")
}
