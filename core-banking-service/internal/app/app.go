package app

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/danielgtaylor/huma/v2"
	"github.com/danielgtaylor/huma/v2/adapters/humago"
	"github.com/jackc/pgx/v5"

	"core-banking-service/internal/customer"
	"core-banking-service/internal/login"
)

type App struct {
	db     *pgx.Conn
	server *http.Server
}

func New() (*App, error) {
	ctx := context.Background()

	databaseURL := os.Getenv("DATABASE_URL")
	if databaseURL == "" {
		return nil, fmt.Errorf("DATABASE_URL is not set")
	}

	db, err := pgx.Connect(ctx, databaseURL)
	if err != nil {
		return nil, fmt.Errorf("connect to database: %w", err)
	}

	if err := db.Ping(ctx); err != nil {
		db.Close(ctx)
		return nil, fmt.Errorf("ping database: %w", err)
	}
	//login service

	loginServiceURL := os.Getenv("LOGIN_SERVICE_URL")

	if loginServiceURL == "" {
		log.Fatal("LOGIN_SERVICE_URL is required sfsdfs")
	}

	loginClient := login.NewClient(loginServiceURL)

	customerRepository := customer.NewCustomerRepository(db)
	customerService := customer.NewCustomerService(customerRepository, loginClient)
	customerHandler := customer.NewCustomerHandler(customerService)

	mux := http.NewServeMux()

	api := humago.New(mux, huma.DefaultConfig("Core Banking Service", "1.0.0"))
	customer.RegisterRoutes(api, "/api/v1/core", customerHandler)

	// -------------------------
	// HTTP server
	// -------------------------

	server := &http.Server{
		Addr: ":8080",

		Handler: loggingMiddleware(mux),
	}

	return &App{
		db:     db,
		server: server,
	}, nil
}

func (a *App) Run() error {
	defer a.db.Close(context.Background())

	return a.server.ListenAndServe()
}

type responseWriter struct {
	http.ResponseWriter
	statusCode int
}

func loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()

		writer := &responseWriter{
			ResponseWriter: w,
			statusCode:     http.StatusOK,
		}

		next.ServeHTTP(writer, r)

		duration := time.Since(start)

		log.Printf(
			"%s %s %d %s",
			r.Method,
			r.URL.RequestURI(),
			writer.statusCode,
			duration,
		)
	})
}
