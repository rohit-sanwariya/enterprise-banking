package main

import (
	"context"
	"log"
	"os"
	"strconv"

	"github.com/brianvoe/gofakeit/v7"
	"github.com/jackc/pgx/v5"

	"core-banking-service/internal/customer"
)

func main() {
	if len(os.Args) != 2 {
		log.Fatal("usage: go run ./cmd/seedcustomer <count>")
	}

	count, err := strconv.Atoi(os.Args[1])
	if err != nil || count <= 0 {
		log.Fatal("count must be a positive integer")
	}

	databaseURL := os.Getenv("DATABASE_URL")
	if databaseURL == "" {
		log.Fatal("DATABASE_URL is not set")
	}

	ctx := context.Background()

	db, err := pgx.Connect(ctx, databaseURL)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close(ctx)

	repository := customer.NewCustomerRepository(db)
	service := customer.NewCustomerService(repository)

	for i := 0; i < count; i++ {
		firstName := gofakeit.FirstName()
		lastName := gofakeit.LastName()
		email := gofakeit.Email()
		phone := gofakeit.Phone()

		_, err := service.Create(
			ctx,
			customer.CustomerTypeIndividual,
			firstName,
			nil,
			lastName,
			nil,
			email,
			&phone,
		)
		if err != nil {
			log.Fatalf("failed to create customer %d: %v", i+1, err)
		}
	}

	log.Printf("created %d customers", count)
}
