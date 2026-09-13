package storage

import (
	"context"
	"fmt"
	"os"

	"github.com/jackc/pgx/v5"
)


func ConnectPostgres(ctx context.Context) (*pgx.Conn, error){

	databaseURL := os.Getenv("DATABASE_URL")

	conn,err := pgx.Connect(ctx , databaseURL)

	if err != nil {
		return nil,fmt.Errorf("connect to postgres failed: %w", err)
	}

	if err := conn.Ping(ctx);err != nil{
		conn.Close(ctx)
		return nil, fmt.Errorf("ping postgres failed: %w",err)
	}

	return conn,nil


}