package proxy

import (
	"api-gateway/config"
	"net/http/httptest"
	"testing"
)

func TestRouterMatch(t *testing.T) {
	routes := []config.Route{
		{
			Path:    "/api/v1/login",
			Service: "login",
		},
		{
			Path:    "/api/v1/core",
			Service: "core-banking",
		},
	}

	router := NewRouter(routes)

	tests := []struct {
		name        string
		path        string
		wantService string
		wantMatch   bool
	}{
		{
			name:        "login",
			path:        "/api/v1/login",
			wantService: "login",
			wantMatch:   true,
		},
		{
			name:        "core customers",
			path:        "/api/v1/core/customers",
			wantService: "core-banking",
			wantMatch:   true,
		},
		{
			name:        "core customer detail",
			path:        "/api/v1/core/customers/123",
			wantService: "core-banking",
			wantMatch:   true,
		},
		{
			name:      "similar but invalid core path",
			path:      "/api/v1/corefoo",
			wantMatch: false,
		},
		{
			name:      "unknown route",
			path:      "/api/v1/unknown",
			wantMatch: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			req := httptest.NewRequest("GET", tt.path, nil)

			route, ok := router.Match(req)

			if ok != tt.wantMatch {
				t.Fatalf("match = %v, want %v", ok, tt.wantMatch)
			}

			if tt.wantMatch && route.Service != tt.wantService {
				t.Fatalf(
					"service = %q, want %q",
					route.Service,
					tt.wantService,
				)
			}
		})
	}
}
