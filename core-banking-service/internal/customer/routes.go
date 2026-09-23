package customer

import (
	"net/http"
)

func RegisterRoutes(
	mux *http.ServeMux,
	handler *CustomerHandler,
) {
	mux.HandleFunc("POST /customers", handler.Create)
	mux.HandleFunc("GET /customers", handler.List)
	mux.HandleFunc("DELETE /customers/{customerNumber}", handler.Delete)
}
