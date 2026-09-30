package auth

import (
	"strings"
	"testing"
)

func TestCreateIdentityQueryUsesCustomerIDColumn(t *testing.T) {
	if strings.Contains(createIdentityQuery, "customer_idEn") {
		t.Fatalf("createIdentityQuery contains a typo in the RETURNING clause: %s", createIdentityQuery)
	}

	if !strings.Contains(createIdentityQuery, "RETURNING id, email, password_hash, customer_id") {
		t.Fatalf("createIdentityQuery is missing the customer_id column in RETURNING: %s", createIdentityQuery)
	}
}
