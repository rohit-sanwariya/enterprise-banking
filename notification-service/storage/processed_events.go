package storage

import (
	"context"
	"log"
	"github.com/jackc/pgx/v5"
)

func EventAlreadyProcessed(
	ctx context.Context,
	conn *pgx.Conn,
	eventID string,
) (bool, error) {
	var exists bool

	err := conn.QueryRow(
		ctx,
		`
		SELECT EXISTS (
			SELECT 1
			FROM processed_events
			WHERE event_id = $1
		)
		`,
		eventID,
	).Scan(&exists)

	if err != nil {
		return false, err
	}
	log.Println("🔥 HOT RELOAD TEST")
	return exists, nil
}

func MarkEventProcessed(
	ctx context.Context,
	conn *pgx.Conn,
	eventID string,
) error {
	_, err := conn.Exec(
		ctx,
		`
		INSERT INTO processed_events (event_id)
		VALUES ($1)
		ON CONFLICT (event_id) DO NOTHING
		`,
		eventID,
	)

	return err
}