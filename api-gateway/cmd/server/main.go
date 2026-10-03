package main

import (
	"context"
	"log"
	"net/http"
	"os"

	"api-gateway/internal/cache"
)

func main() {
	redisURL := os.Getenv("REDIS_URL")
	if redisURL == "" {
		redisURL = "redis://localhost:6379"
	}

	redisClient, err := cache.NewRedisClient(redisURL)
	if err != nil {
		log.Fatalf("failed to create redis client: %v", err)
	}
	defer redisClient.Close()

	if err := redisClient.Ping(context.Background()); err != nil {
		log.Fatalf("failed to connect to redis: %v", err)
	}

	log.Println("Redis connection established")

	mux := http.NewServeMux()

	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(`{"status":"ok"}`))
	})

	server := &http.Server{
		Addr:    ":8080",
		Handler: mux,
	}

	log.Println("API Gateway listening on :8080")

	if err := server.ListenAndServe(); err != nil {
		log.Fatal(err)
	}
}
