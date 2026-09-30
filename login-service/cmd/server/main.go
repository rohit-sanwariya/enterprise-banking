package main

import (
	"context"
	"log"
	"login-service/internal/auth"
	"login-service/internal/database"
	"net/http"
	"os"

	"github.com/go-chi/chi/v5"
)

func main() {
		ctx := context.Background()

	databaseURL := os.Getenv("DATABASE_URL")
	if databaseURL == "" {
		log.Fatal("DATABASE_URL is required")
	}

	db, err := database.NewPostgresPool(ctx, databaseURL)
	if err != nil {
		log.Fatalf("connect to database: %v", err)
	}
	defer db.Close()
	router := chi.NewRouter()
	authRepository := auth.NewRepository(db)
	authService := auth.NewService(authRepository)
authHandler := auth.NewHandler(authService)
	router.Get("/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte("OK"))
	})
	router.Route("/auth", func(r chi.Router) {
		r.Post("/register", authHandler.Register)
	})
	server := &http.Server{
		Addr:    ":8080",
		Handler: router,
	}

	log.Println("air for dev, login service listening on :8080")

	if err := server.ListenAndServe(); err != nil {
		log.Fatal(err)
	}
}