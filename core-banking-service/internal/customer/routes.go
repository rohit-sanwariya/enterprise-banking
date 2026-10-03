package customer

import (
	"net/http"

	"github.com/danielgtaylor/huma/v2"
)

func RegisterRoutes(
	api huma.API,
	prefix string,
	handler *CustomerHandler,
) {
	huma.Register(api, huma.Operation{
		OperationID: "create-customer",
		Method:      http.MethodPost,
		Path:        prefix + "/customers",
		Summary:     "Create a customer",
		Tags:        []string{"customers"},
		Errors:      []int{http.StatusBadRequest},
	}, handler.Create)

	huma.Register(api, huma.Operation{
		OperationID: "list-customers",
		Method:      http.MethodGet,
		Path:        prefix + "/customers",
		Summary:     "List customers",
		Tags:        []string{"customers"},
		Errors:      []int{http.StatusBadRequest, http.StatusInternalServerError},
	}, handler.List)

	huma.Register(api, huma.Operation{
		OperationID: "delete-customer",
		Method:      http.MethodDelete,
		Path:        prefix + "/customers/{customerNumber}",
		Summary:     "Delete a customer",
		Tags:        []string{"customers"},
		Errors:      []int{http.StatusBadRequest, http.StatusInternalServerError},
	}, handler.Delete)
}
