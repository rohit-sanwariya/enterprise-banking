package login

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"uuid"
)

type Client struct {
	baseURL    string
	httpClient *http.Client
}

func NewClient(baseURL string) *Client {
	return &Client{
		baseURL:    baseURL,
		httpClient: &http.Client{},
	}
}

type ProvisionIdentityRequest struct {
	Email      string    `json:"email"`
	CustomerID uuid.UUID `json:"customer_id"`
	Password   string    `json:"password"`
}

type ProvisionIdentityResponse struct {
	ID    uuid.UUID `json:"id"`
	Email string    `json:"email"`
}

func (c *Client) ProvisionIdentity(
	ctx context.Context,
	customerId uuid.UUID,
	email string,
	password string,
) (*ProvisionIdentityResponse, error) {
	var response ProvisionIdentityResponse

	requestBody := ProvisionIdentityRequest{
		Email:      email,
		Password:   password,
		CustomerID: customerId,
	}

	body, err := json.Marshal(requestBody)
	if err != nil {
		return nil, fmt.Errorf("Marshal Identity Request: %w", err)
	}
	log.Print("THE BASE_URL", c.baseURL)
	req, err := http.NewRequestWithContext(
		ctx,
		http.MethodPost,
		c.baseURL+"/auth/register",
		bytes.NewReader(body),
	)
	if err != nil {
		return nil, fmt.Errorf("create Identity Request: %w", err)
	}

	req.Header.Set("Content-Type", "application/json")

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("provision identity: %w", err)
	}

	defer resp.Body.Close()

	if resp.StatusCode != http.StatusCreated {
		return nil, fmt.Errorf("login service returned status %d", resp.StatusCode)
	}

	if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
		return nil, fmt.Errorf("decode identity response : %w", err)
	}

	return &response, nil
}
