package auth

import (
	"context"
	"fmt"
	"uuid"
)

type Service struct {
	repository *Repository
}

func NewService(repo *Repository) *Service {
	return &Service{
		repository: repo,
	}
}

func (svc *Service) Register(
	ctx context.Context,
	email string,
	password string,
	customerID uuid.UUID,

) ( *Identity, error){
	passwordHash,err := HashPassword(password)
		if err != nil {
		return nil,fmt.Errorf("Service failed to create = %w", err)
	}
	identity,err := svc.repository.CreateIdentity(
		ctx,
		email,
		passwordHash,
		customerID,
	)

	if err != nil {
		return nil,fmt.Errorf("Service failed to create = %w", err)
	}

	return identity,err


}