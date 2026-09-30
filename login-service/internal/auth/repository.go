package auth

import (
	"context"
	"fmt"
	"uuid"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
)

type Identity struct {
	ID uuid.UUID
	CustomerID   uuid.UUID
	Email string
	PasswordHash string 
}


type Repository struct {
	db *pgxpool.Pool 
}

func NewRepository(db *pgxpool.Pool) *Repository{
	return &Repository{
		db:db,
	}
}


func (r *Repository) CreateIdentity(
	ctx context.Context,
	email string,
	passwordHash string,
	customerID uuid.UUID,
) (*Identity,error) {
	identity := &Identity{}
	id := uuid.New()
	args := pgx.NamedArgs{
		"id": id,
		"email": email,
		"password_hash" : passwordHash,
		"customer_id" : customerID,
	}

	err := r.db.QueryRow(
		ctx, createIdentityQuery, args,
	).Scan(
		&identity.ID,
		&identity.Email,
		&identity.PasswordHash,
		&identity.CustomerID,
	)

	if err != nil {
		return nil, fmt.Errorf("create identity: %w", err)
	}
	return identity, nil
}