package app

import (
	"context"
	"fmt"
	"net/http"
	"os"
	"time"
	"log"
	"github.com/jackc/pgx/v5"
	httpSwagger "github.com/swaggo/http-swagger/v2"

	"core-banking-service/internal/customer"

	_ "core-banking-service/docs"
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

	// -------------------------
	// Customer dependencies
	// -------------------------

	customerRepository := customer.NewCustomerRepository(db)
	customerService := customer.NewCustomerService(customerRepository)
	customerHandler := customer.NewCustomerHandler(customerService)

	// -------------------------
	// HTTP routes
	// -------------------------

	mux := http.NewServeMux()

	mux.Handle(
		"/swagger/",
		httpSwagger.Handler(
			httpSwagger.URL("/swagger/doc.json"),
		),
	)

	customer.RegisterRoutes(mux, customerHandler)

	// -------------------------
	// HTTP server
	// -------------------------

	server := &http.Server{
		Addr:    ":8080",
		
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