package main

import (
	"context"
	"log"
	"net/http"
	"os"

	"api-gateway/config"
	"api-gateway/internal/cache"
	"api-gateway/internal/proxy"
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
	cfg, err := config.LoadRoutes("config/gateway-routes.yaml")
	if err != nil {
		log.Fatalf("failed to load gateway routes: %v", err)
	}

	router := proxy.NewRouter(cfg.Routes)

	proxies := make(map[string]http.Handler)

	for name, service := range cfg.Services {
		serviceProxy, err := proxy.NewProxy(service)
		if err != nil {
			log.Fatalf(
				"failed to create proxy for service %q: %v",
				name,
				err,
			)
		}

		proxies[name] = serviceProxy
	}

	gatewayHandler := proxy.NewHandler(router, proxies)
	mux := http.NewServeMux()
	mux.Handle("/api/", gatewayHandler)
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
