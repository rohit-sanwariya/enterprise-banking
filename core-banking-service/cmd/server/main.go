package main

import (
	"core-banking-service/internal/app"
	"log"
)

func main() {
	application, err := app.New()
	if err != nil {
		log.Fatal(err)
	}
	log.Println("HTTP server listening on :8080")

	if err := application.Run(); err != nil {
		log.Fatal(err)
	}
}
