package main

import (
	"context"
	"log"
	"os"

	"notification-service/consumer"
	"notification-service/email"
	"notification-service/messaging"
	"notification-service/storage"
)

func main() {
	ctx := context.Background()

	db, err := storage.ConnectPostgres(ctx)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close(ctx)

	log.Println("connected to PostgreSQL")

	rabbitMQURL := os.Getenv("RABBITMQ_URL")

	conn, ch, err := messaging.Connect(rabbitMQURL)
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()
	defer ch.Close()

	if err := messaging.Setup(ch); err != nil {
		log.Fatal(err)
	}

	emailSender := email.NewSender(
		os.Getenv("SMTP_HOST"),
		os.Getenv("SMTP_PORT"),
		os.Getenv("SMTP_FROM"),
	)

	c := consumer.New(ch, db, emailSender)

	if err := c.Start(ctx); err != nil {
		log.Fatal(err)
	}
}
