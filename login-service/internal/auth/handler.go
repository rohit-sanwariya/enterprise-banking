package auth

import (
	"encoding/json"
	"log"
	"net/http"
	"uuid"

	"github.com/go-playground/validator/v10"
)

type RegisterRequest struct {
	Email      string `json:"email" validate:"required,email"`
	Password   string `json:"password" validate:"required,min=8"`
	CustomerID string `json:"customer_id" validate:"required,uuid"`
}
type RegisterResponse struct {
	ID    uuid.UUID `json:"id"`
	Email string    `json:"email"`
}
type Handler struct {
	service  *Service
	validate *validator.Validate
}

func NewHandler(
	service *Service,
) *Handler {

	return &Handler{
		service:  service,
		validate: validator.New(),
	}
}

func (h *Handler) Register(w http.ResponseWriter, r *http.Request) {
	var request RegisterRequest

	if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
		http.Error(w, "Invalid Request Body", http.StatusBadRequest)
		return
	}

	if err := h.validate.Struct(request); err != nil {
		validationErrors := err.(validator.ValidationErrors)

		for _, fieldError := range validationErrors {
			log.Printf(
				"validation failed: field=%s tag=%s",
				fieldError.Field(),
				fieldError.Tag(),
			)
		}
		http.Error(w, "Invalid Request: field validation failed", http.StatusBadRequest)
		return
	}

	customerIdParsed, err := uuid.Parse(request.CustomerID)
	if err != nil {
		http.Error(w, "Invalid Customer", http.StatusBadRequest)
		return
	}
	identity, err := h.service.Register(
		r.Context(),
		request.Email,
		request.Password,
		customerIdParsed,
	)
	if err != nil {
		http.Error(w, "registration failed", http.StatusInternalServerError)
		return
	}
	response := RegisterResponse{
		ID:    identity.ID,
		Email: identity.Email,
	}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	log.Print(response)
	_ = json.NewEncoder(w).Encode(response)

}
