package customer

import (
	"fmt"
	"net/http"
)

func RegisterRoutes(
	mux *http.ServeMux,
	prefix string,
	handler *CustomerHandler,
) {
	mux.HandleFunc(fmt.Sprintf("POST %s/customers", prefix), handler.Create)
	mux.HandleFunc(fmt.Sprintf("GET %s/customers", prefix), handler.List)
	mux.HandleFunc(fmt.Sprintf("DELETE %s/customers/{customerNumber}", prefix), handler.Delete)
}
