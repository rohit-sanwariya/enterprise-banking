package customer

import (
	"encoding/json"
	"log"
	"net/http"
	"strconv"
	"strings"
)

type CreateCustomerRequest struct {
	CustomerType CustomerType `json:"customer_type"`
	FirstName    string       `json:"first_name"`
	MiddleName   *string      `json:"middle_name"`
	LastName     string       `json:"last_name"`
	DateOfBirth  *string      `json:"date_of_birth"`
	Email        string       `json:"email"`
	PhoneNumber  *string      `json:"phone_number"`
}

type CustomerHandler struct {
	service *CustomerService
}

func NewCustomerHandler(service *CustomerService) *CustomerHandler {
	return &CustomerHandler{
		service: service,
	}
}

// CreateCustomer godoc
// @Summary Create a customer
// @Description Creates a new customer.
// @Tags customers
// @Accept json
// @Produce json
// @Param customer body CreateCustomerRequest true "Customer"
// @Success 201 {object} Customer
// @Failure 400 {string} string
// @Router /customers [post]
func (h *CustomerHandler) Create(w http.ResponseWriter, r *http.Request) {
	var request CreateCustomerRequest

	if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
		http.Error(w, "invalid request body", http.StatusBadRequest)
		return
	}

	customer, err := h.service.Create(
		r.Context(),
		request.CustomerType,
		request.FirstName,
		request.MiddleName,
		request.LastName,
		request.DateOfBirth,
		request.Email,
		request.PhoneNumber,
	)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)

	_ = json.NewEncoder(w).Encode(customer)
}

// GetAllCustomers godoc
// @Summary Get all customers
// @Description Get all customers.
// @Tags customers
// @Produce json
// @Success 200 {array} Customer
// @Failure 500 {string} string
// @Router /customers [get]
// @Param page query int false "Page number" default(1)
// @Param limit query int false "Number of customers per page" default(20)
func (h *CustomerHandler) List(w http.ResponseWriter, r *http.Request) {
	page, err := strconv.Atoi(r.URL.Query().Get("page"))
	if err != nil || page < 1 {
		http.Error(w, "page must be a positive integer", http.StatusBadRequest)
		return
	}
	limit, err := strconv.Atoi(r.URL.Query().Get("limit"))
	if err != nil || limit < 1 || limit > 100 {
		http.Error(w, "limit must be between 1 and 100", http.StatusBadRequest)
		return
	}
	customers, err := h.service.List(r.Context(), page, limit)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	_ = json.NewEncoder(w).Encode(customers)
}

// DeleteCustomer godoc
//
// @Summary Delete Customer by customer number
// @Description Delete Customer by customer number
// @Tags customers
// @Produce json
// @Param customerNumber path string true "Customer number"
// @Success 204
// @Failure 400 {string} string
// @Failure 500 {string} string
// @Router /customers/{customerNumber} [delete]
func (h *CustomerHandler) Delete(w http.ResponseWriter, r *http.Request) {
	customerNumber := r.PathValue("customerNumber")

	if strings.TrimSpace(customerNumber) == "" {
		http.Error(w, "Enter Valid customer number", http.StatusBadRequest)
	}
	err := h.service.Delete(r.Context(), customerNumber)
	if err != nil {
		log.Printf("delete customer failed: %v", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusNoContent)
}
