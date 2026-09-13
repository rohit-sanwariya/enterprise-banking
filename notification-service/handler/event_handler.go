package handler

import (
	"log"
	"encoding/json"
	"fmt"
)


type Event struct {
	EventID    string          `json:"event_id"`
	EventType  string          `json:"event_type"`
	OccurredAt string          `json:"occurred_at"`
	Data       json.RawMessage `json:"data"`
}



func HandleEvent(event Event) error {
	log.Printf(
		"event received: id=%s type=%s occurred_at=%s",
		event.EventID,
		event.EventType,
		event.OccurredAt,
	)

	switch event.EventType {
	case "account.created":
		return handleAccountCreated(event.Data)

	default:
		log.Printf("unknown event type: %s", event.EventType)
		return nil
	}
}


func handleAccountCreated(data json.RawMessage) error{
	log.Printf("handling account.created:%s",data)

	return nil
}


func ParseEvent(body []byte) (Event, error) {
	var event Event

	if err := json.Unmarshal(body, &event); err != nil {
		return Event{}, fmt.Errorf("decode event: %w", err)
	}

	return event, nil
}