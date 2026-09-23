package customer

import (
	"context"

	"github.com/google/uuid"
)

type CustomerService struct {
	repository *CustomerRepository
}

func NewCustomerService(repository *CustomerRepository) *CustomerService {
	return &CustomerService{
		repository: repository,
	}
}
func (s *CustomerService) List(ctx context.Context, page int, limit int) ([]*CustomerListItem, error) {
	customers, err := s.repository.List(ctx, page, limit)
	if err != nil {
		return nil, err
	}

	return customers, nil
}
func (s *CustomerService) Create(
	ctx context.Context,
	customerType CustomerType,
	firstName string,
	middleName *string,
	lastName string,
	dateOfBirth *string,
	email string,
	phoneNumber *string,
) (*Customer, error) {

	parsedDateOfBirth, err := parseDateOfBirth(dateOfBirth)
	if err != nil {
		return nil, err
	}

	if err := validateCreateCustomer(
		customerType,
		firstName,
		middleName,
		lastName,
		email,
		phoneNumber,
	); err != nil {
		return nil, err
	}

	customer := &Customer{
		ID:             uuid.New(),
		CustomerNumber: generateCustomerNumber(),
		CustomerType:   customerType,
		FirstName:      firstName,
		MiddleName:     middleName,
		LastName:       lastName,
		DateOfBirth:    parsedDateOfBirth,
		Email:          email,
		PhoneNumber:    phoneNumber,
		Status:         CustomerStatusActive,
	}

	err = s.repository.Create(ctx, customer)
	if err != nil {
		return nil, err
	}

	return customer, nil
}

func (s *CustomerService) Delete(ctx context.Context, customerNumber string) error {

	err := s.repository.Delete(ctx, customerNumber)

	return err
}
