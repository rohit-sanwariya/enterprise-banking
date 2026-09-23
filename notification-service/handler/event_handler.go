package handler

import (
	"bytes"
	"encoding/json"
	"fmt"
	"html/template"
	"log"

	"notification-service/email"
)

type Event struct {
	EventID    string          `json:"event_id"`
	EventType  string          `json:"event_type"`
	OccurredAt string          `json:"occurred_at"`
	Data       json.RawMessage `json:"data"`
}

type AccountCreatedData struct {
	AccountID  string `json:"account_id"`
	CustomerID string `json:"customer_id"`
	Email      string `json:"email"`
}

func HandleEvent(event Event, emailSender *email.Sender) error {
	log.Printf(
		"event received: id=%s type=%s occurred_at=%s",
		event.EventID,
		event.EventType,
		event.OccurredAt,
	)

	switch event.EventType {
	case "account.created":
		return handleAccountCreated(event.Data, emailSender)

	default:
		log.Printf("unknown event type: %s", event.EventType)
		return nil
	}
}

func handleAccountCreated(
	data json.RawMessage,
	emailSender *email.Sender,
) error {
	var account AccountCreatedData

	if err := json.Unmarshal(data, &account); err != nil {
		return fmt.Errorf("decode account.created data: %w", err)
	}

	log.Printf(
		"account created: account_id=%s customer_id=%s email=%s",
		account.AccountID,
		account.CustomerID,
		account.Email,
	)

	subject := "Your bank account has been created"

	tmpl, err := template.ParseFiles("email/templates/account_created.html")
	if err != nil {
		return fmt.Errorf("parse account created email template: %w", err)
	}

	var body bytes.Buffer

	if err := tmpl.Execute(&body, account); err != nil {
		return fmt.Errorf("execute account created email template: %w", err)
	} 

	if err := emailSender.Send(
		account.Email,
		subject,
		body.String(),
	); err != nil {
		return fmt.Errorf("send account created email: %w", err)
	}

	log.Printf("account created email sent to %s", account.Email)

	return nil
}

func ParseEvent(body []byte) (Event, error) {
	var event Event

	if err := json.Unmarshal(body, &event); err != nil {
		return Event{}, fmt.Errorf("decode event: %w", err)
	}

	return event, nil
}