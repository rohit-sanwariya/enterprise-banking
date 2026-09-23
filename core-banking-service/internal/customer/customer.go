package customer

import (
	"core-banking-service/internal/common"
	"github.com/google/uuid"
	"time"
)

type CustomerType string

const (
	CustomerTypeIndividual CustomerType = "INDIVIDUAL"
	CustomerTypeBusiness   CustomerType = "BUSINESS"
)

type CustomerStatus string

const (
	CustomerStatusActive   CustomerStatus = "ACTIVE"
	CustomerStatusClosed   CustomerStatus = "CLOSED"
	CustomerStatusDormant  CustomerStatus = "DORMANT"
	CustomerStatusFrozen   CustomerStatus = "FROZEN"
	CustomerStatusDeceased CustomerStatus = "DECEASED"
)

type Customer struct {
	ID             uuid.UUID
	CustomerNumber string
	CustomerType   CustomerType
	FirstName      string
	MiddleName     *string
	LastName       string
	DateOfBirth    *time.Time
	Email          string
	PhoneNumber    *string
	Status         CustomerStatus

	common.Timestamp
	common.SoftDelete
}

type CustomerListItem struct {
	CustomerNumber string         `json:"customer_number"`
	CustomerType   CustomerType   `json:"customer_type"`
	FirstName      string         `json:"first_name"`
	MiddleName     *string        `json:"middle_name"`
	LastName       string         `json:"last_name"`
	DateOfBirth    *time.Time     `json:"date_of_birth,omitempty"`
	Email          string         `json:"email"`
	PhoneNumber    *string        `json:"phone_number,omitempty"`
	Status         CustomerStatus `json:"status"`
	CreatedAt      time.Time      `json:"created_at"`
}
