package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/gin-gonic/gin"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func main() {
	router := gin.Default()

	router.GET("/secrets/:secret", func(c *gin.Context) {
		secret := c.Param("secret")

		client, ctx := mongoConnect("mongodb://127.0.0.1:27017")
		defer client.Disconnect(ctx)

		collection := client.Database("alcazar").Collection("secrets")

		var result struct {
			Value string
		}

		err := collection.FindOne(ctx, bson.D{{"name", secret}}).Decode(&result)
		if err != nil {
			fmt.Printf("%s", err)
			c.JSON(404, gin.H{
				"error": "Could not find secret",
			})
			return
		}

		c.JSON(200, gin.H{
			"name":  secret,
			"value": result.Value,
		})
	})

	router.POST("/secrets/:secret", func(c *gin.Context) {
		secret := c.Param("secret")
		secret_value := c.PostForm("value")

		client, ctx := mongoConnect("mongodb://127.0.0.1:27017")
		defer client.Disconnect(ctx)

		collection := client.Database("alcazar").Collection("secrets")

		res, err := collection.InsertOne(ctx, bson.D{{"name", secret}, {"value", secret_value}})
		if err != nil {
			fmt.Printf("%s", err)
			c.JSON(500, gin.H{
				"error": err,
			})
			return
		}

		c.JSON(200, gin.H{
			"secret": secret,
			"result": res,
		})
	})

	router.PATCH("/secrets/:secret", func(c *gin.Context) {
		secret := c.Param("secret")
		new_secret_value := c.PostForm("value")

		client, ctx := mongoConnect("mongodb://127.0.0.1:27017")
		defer client.Disconnect(ctx)

		collection := client.Database("alcazar").Collection("secrets")

		res, err := collection.UpdateOne(ctx, bson.D{{"name", secret}}, bson.D{{"$set", bson.D{{"value", new_secret_value}}}})
		if err != nil {
			fmt.Printf("%s", err)
			c.JSON(500, gin.H{
				"error": err,
			})
			return
		}

		c.JSON(200, gin.H{
			"secret": secret,
			"result": res,
		})
	})

	router.DELETE("/secrets/:secret", func(c *gin.Context) {
		secret := c.Param("secret")

		client, ctx := mongoConnect("mongodb://127.0.0.1:27017")
		defer client.Disconnect(ctx)

		collection := client.Database("alcazar").Collection("secrets")

		res, err := collection.DeleteOne(ctx, bson.D{{"name", secret}})
		if err != nil {
			fmt.Printf("%s", err)
			c.JSON(500, gin.H{
				"error": err,
			})
			return
		}

		c.JSON(200, gin.H{
			"secret": secret,
			"result": res,
		})
	})

	router.Run(":8080")
}

func mongoConnect(dbURI string) (mongo.Client, context.Context) {
	// Connect to mongodb
	client, err := mongo.NewClient(options.Client().ApplyURI("mongodb://127.0.0.1:27017"))
	if err != nil {
		log.Fatal(err)
	}

	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
	err = client.Connect(ctx)
	if err != nil {
		log.Fatal(err)
	}

	return *client, ctx
}
