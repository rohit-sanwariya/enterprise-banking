package customer

import (
	"errors"
	"fmt"
	"net/mail"
	"strings"
	"time"
	"unicode/utf8"
)

func parseDateOfBirth(value *string) (*time.Time, error) {
	if value == nil || strings.TrimSpace(*value) == "" {
		return nil, nil
	}

	date, err := time.Parse("2006-01-02", *value)
	if err != nil {
		return nil, errors.New("invalid date of birth, expected YYYY-MM-DD")
	}

	return &date, nil
}
func validateCreateCustomer(
	customerType CustomerType,
	firstName string,
	middleName *string,
	lastName string,
	email string,
	phoneNumber *string,
) error {

	if customerType != CustomerTypeIndividual &&
		customerType != CustomerTypeBusiness {
		return errors.New("invalid customer type")
	}

	if strings.TrimSpace(firstName) == "" {
		return errors.New("first name is required")
	}

	if utf8.RuneCountInString(firstName) > 100 {
		return errors.New("first name must not exceed 100 characters")
	}

	if middleName != nil && utf8.RuneCountInString(*middleName) > 100 {
		return errors.New("middle name must not exceed 100 characters")
	}

	if strings.TrimSpace(lastName) == "" {
		return errors.New("last name is required")
	}

	if utf8.RuneCountInString(lastName) > 100 {
		return errors.New("last name must not exceed 100 characters")
	}

	if strings.TrimSpace(email) == "" {
		return errors.New("email is required")
	}

	if utf8.RuneCountInString(email) > 255 {
		return errors.New("email must not exceed 255 characters")
	}

	if _, err := mail.ParseAddress(email); err != nil {
		return fmt.Errorf("invalid email: %w", err)
	}

	if phoneNumber != nil && utf8.RuneCountInString(*phoneNumber) > 20 {
		return errors.New("phone number must not exceed 20 characters")
	}

	return nil
}
