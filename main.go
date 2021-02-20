package main

import "github.com/gin-gonic/gin"

func main() {
	router := gin.Default()

	router.GET("/secrets/:secret", func(c *gin.Context) {
		secret := c.Param("secret")

		c.JSON(200, gin.H{
			"secret": secret,
		})
	})

	router.POST("/secrets/:secret", func(c *gin.Context) {
		secret := c.Param("secret")

		c.JSON(200, gin.H{
			"secret": secret,
		})
	})

	router.PATCH("/secrets/:secret", func(c *gin.Context) {
		secret := c.Param("secret")

		c.JSON(200, gin.H{
			"secret": secret,
		})
	})

	router.DELETE("/secrets/:secret", func(c *gin.Context) {
		secret := c.Param("secret")

		c.JSON(200, gin.H{
			"secret": secret,
		})
	})

	router.Run(":8080")
}
