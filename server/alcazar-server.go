/* Server-side secret storage w/ mongodb */

package main

import (
	"context"
	"crypto/sha1"
	"encoding/hex"
	"fmt"
	"log"
	"time"

	"github.com/gin-gonic/gin"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

const MongoURI string = "mongodb://127.0.0.1:27017"

func main() {
	router := gin.Default()

	router.GET("/secrets/:secret", func(c *gin.Context) {
		secretName := c.Param("secret")

		secretNameHash := sha1.Sum([]byte(secretName))
		_id := hex.EncodeToString(secretNameHash[:])

		client, mongoContext := mongoConnect(MongoURI)
		defer client.Disconnect(mongoContext)

		collection := client.Database("alcazar").Collection("secrets")

		var result struct {
			Value string
		}

		err := collection.FindOne(mongoContext, bson.D{{"_id", _id}}).Decode(&result)
		if err != nil {
			fmt.Printf("%s", err)
			c.JSON(404, gin.H{
				"error": "Could not find secret",
			})
			return
		}

		c.JSON(200, gin.H{
			"name":  secretName,
			"value": result.Value,
		})
	})

	router.POST("/secrets/:secret", func(c *gin.Context) {
		secretName := c.Param("secret")
		secretValue := c.PostForm("value")

		secretNameHash := sha1.Sum([]byte(secretName))
		_id := hex.EncodeToString(secretNameHash[:]) // use hash of secretName as _id in mongodb

		client, mongoContext := mongoConnect(MongoURI)
		defer client.Disconnect(mongoContext)

		collection := client.Database("alcazar").Collection("secrets")

		res, err := collection.InsertOne(mongoContext, bson.D{{"_id", _id}, {"name", secretName}, {"value", secretValue}})
		if err != nil {
			fmt.Printf("%s", err)
			c.JSON(500, gin.H{
				"error": err,
			})
			return
		}

		c.JSON(200, gin.H{
			"secret": secretName,
			"result": res,
		})
	})

	router.PATCH("/secrets/:secret", func(c *gin.Context) {
		secretName := c.Param("secret")
		newSecretValue := c.PostForm("value")

		secretNameHash := sha1.Sum([]byte(secretName))
		_id := hex.EncodeToString(secretNameHash[:])

		client, mongoContext := mongoConnect(MongoURI)
		defer client.Disconnect(mongoContext)

		collection := client.Database("alcazar").Collection("secrets")

		res, err := collection.UpdateOne(mongoContext, bson.D{{"_id", _id}}, bson.D{{"$set", bson.D{{"value", newSecretValue}}}})
		if err != nil {
			fmt.Printf("%s", err)
			c.JSON(500, gin.H{
				"error": err,
			})
			return
		}

		c.JSON(200, gin.H{
			"secret": secretName,
			"result": res,
		})
	})

	router.DELETE("/secrets/:secret", func(c *gin.Context) {
		secretName := c.Param("secret")

		secretNameHash := sha1.Sum([]byte(secretName))
		_id := hex.EncodeToString(secretNameHash[:])

		client, mongoContext := mongoConnect(MongoURI)
		defer client.Disconnect(mongoContext)

		collection := client.Database("alcazar").Collection("secrets")

		res, err := collection.DeleteOne(mongoContext, bson.D{{"_id", _id}})
		if err != nil {
			fmt.Printf("%s", err)
			c.JSON(500, gin.H{
				"error": err,
			})
			return
		}

		c.JSON(204, gin.H{
			"secret": secretName,
			"result": res,
		})
	})

	router.Run(":8080")
	// log.Fatal(autotls.Run(router, ":8080"))
}

func mongoConnect(dbURI string) (mongo.Client, context.Context) {
	// Connect to mongodb
	client, err := mongo.NewClient(options.Client().ApplyURI(dbURI))
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
