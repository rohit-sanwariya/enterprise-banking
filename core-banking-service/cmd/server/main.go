package main

import (
	"log"

	"core-banking-service/internal/app"
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