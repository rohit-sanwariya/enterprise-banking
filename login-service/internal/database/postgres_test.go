package database

import (
	"context"
	"os"
	"testing"
	"time"
)

func TestNewPostgresPool(t *testing.T){
	databaseURL := os.Getenv("DATABASE_URL")

	if databaseURL == "" {
		t.Skip("DATABASE_URL is not set in env")
	}

	ctx, cancel := context.WithTimeout(context.Background(),5*time.Second)

	defer cancel()

	pool, err := NewPostgresPool(ctx,databaseURL)

	if err != nil {
		t.Fatalf("NewPostgresPool() error %v",err)
	}

	defer pool.Close()

	if err := pool.Ping(ctx); err != nil {
		t.Fatalf("database ping failed: %v", err)
	}
}