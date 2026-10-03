package customer

import (
	"context"
	"log"
	"net/http"
	"strings"

	"github.com/danielgtaylor/huma/v2"
)

type CreateCustomerRequest struct {
	CustomerType CustomerType `json:"customer_type"`
	FirstName    string       `json:"first_name"`
	MiddleName   *string      `json:"middle_name"`
	LastName     string       `json:"last_name"`
	DateOfBirth  *string      `json:"date_of_birth"`
	Email        string       `json:"email"`
	Password     string       `json:"password"`
	PhoneNumber  *string      `json:"phone_number"`
}

type CustomerHandler struct {
	service *CustomerService
}

type CreateCustomerInput struct {
	Body CreateCustomerRequest
}

type CreateCustomerOutput struct {
	Status int `status:"201"`
	Body   *Customer
}

type ListCustomersInput struct {
	Page  int `query:"page" required:"true" minimum:"1"`
	Limit int `query:"limit" required:"true" minimum:"1" maximum:"100"`
}

type ListCustomersOutput struct {
	Body []*CustomerListItem
}

type DeleteCustomerInput struct {
	CustomerNumber string `path:"customerNumber"`
}

type DeleteCustomerOutput struct {
	Status int `status:"204"`
}

func NewCustomerHandler(service *CustomerService) *CustomerHandler {
	return &CustomerHandler{
		service: service,
	}
}

func (h *CustomerHandler) Create(ctx context.Context, input *CreateCustomerInput) (*CreateCustomerOutput, error) {
	request := input.Body
	customer, err := h.service.Create(
		ctx,
		request.CustomerType,
		request.FirstName,
		request.MiddleName,
		request.LastName,
		request.DateOfBirth,
		request.Email,
		request.PhoneNumber,
		request.Password,
	)
	if err != nil {
		return nil, huma.NewError(http.StatusBadRequest, err.Error())
	}

	return &CreateCustomerOutput{
		Status: http.StatusCreated,
		Body:   customer,
	}, nil
}

func (h *CustomerHandler) List(ctx context.Context, input *ListCustomersInput) (*ListCustomersOutput, error) {
	if input.Page < 1 {
		return nil, huma.NewError(http.StatusBadRequest, "page must be a positive integer")
	}
	if input.Limit < 1 || input.Limit > 100 {
		return nil, huma.NewError(http.StatusBadRequest, "limit must be between 1 and 100")
	}
	customers, err := h.service.List(ctx, input.Page, input.Limit)
	if err != nil {
		return nil, huma.NewError(http.StatusInternalServerError, err.Error())
	}

	return &ListCustomersOutput{Body: customers}, nil
}

func (h *CustomerHandler) Delete(ctx context.Context, input *DeleteCustomerInput) (*DeleteCustomerOutput, error) {
	customerNumber := input.CustomerNumber
	if strings.TrimSpace(customerNumber) == "" {
		return nil, huma.NewError(http.StatusBadRequest, "Enter Valid customer number")
	}
	err := h.service.Delete(ctx, customerNumber)
	if err != nil {
		log.Printf("delete customer failed: %v", err)
		return nil, huma.NewError(http.StatusInternalServerError, err.Error())
	}

	return &DeleteCustomerOutput{Status: http.StatusNoContent}, nil
}
