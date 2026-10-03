package customer

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/danielgtaylor/huma/v2"
	"github.com/danielgtaylor/huma/v2/adapters/humago"
)

func TestRegisterRoutesPublishesOpenAPI(t *testing.T) {
	mux := http.NewServeMux()
	api := humago.New(mux, huma.DefaultConfig("Core Banking Service", "1.0.0"))
	RegisterRoutes(api, "/api/v1", NewCustomerHandler(nil))

	response := httptest.NewRecorder()
	mux.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "/openapi.json", nil))
	if response.Code != http.StatusOK {
		t.Fatalf("GET /openapi.json returned %d: %s", response.Code, response.Body.String())
	}

	var document struct {
		Paths map[string]map[string]json.RawMessage `json:"paths"`
	}
	if err := json.Unmarshal(response.Body.Bytes(), &document); err != nil {
		t.Fatalf("decode OpenAPI document: %v", err)
	}

	for _, endpoint := range []struct {
		path   string
		method string
	}{
		{path: "/api/v1/customers", method: "post"},
		{path: "/api/v1/customers", method: "get"},
		{path: "/api/v1/customers/{customerNumber}", method: "delete"},
	} {
		if _, ok := document.Paths[endpoint.path][endpoint.method]; !ok {
			t.Errorf("OpenAPI document is missing %s %s", endpoint.method, endpoint.path)
		}
	}
}
