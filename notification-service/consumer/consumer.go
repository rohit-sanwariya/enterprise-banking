package consumer

import (
	"context"
	"log"

	"github.com/jackc/pgx/v5"
	"github.com/rabbitmq/amqp091-go"

	"notification-service/handler"
	"notification-service/storage"
)

type Consumer struct {
	channel *amqp091.Channel
	db      *pgx.Conn
}

func New(channel *amqp091.Channel, db *pgx.Conn) *Consumer {
	return &Consumer{
		channel: channel,
		db:      db,
	}
}

func (c *Consumer) Start(ctx context.Context) error {
	messages, err := c.channel.Consume(
		"notifications",
		"",
		false, // manual ACK
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		return err
	}

	log.Println("waiting for messages...")

	for message := range messages {
		if err := c.processMessage(ctx, message); err != nil {
			log.Printf("failed to process message: %v", err)
		}
	}

	return nil
}

func (c *Consumer) processMessage(
	ctx context.Context,
	message amqp091.Delivery,
) error {
	event, err := handler.ParseEvent(message.Body)
	if err != nil {
		// Invalid message won't become valid by retrying.
		if nackErr := message.Nack(false, false); nackErr != nil {
			log.Printf("failed to nack invalid message: %v", nackErr)
		}

		return err
	}

	log.Printf("event parsed: %s", event.EventID)

	processed, err := storage.EventAlreadyProcessed(
		ctx,
		c.db,
		event.EventID,
	)
	if err != nil {
		// Database failure is potentially temporary.
		if nackErr := message.Nack(false, true); nackErr != nil {
			log.Printf("failed to nack message: %v", nackErr)
		}

		return err
	}

 

	if processed {
		log.Printf("event already processed: %s", event.EventID)

		if err := message.Ack(false); err != nil {
			return err
		}

		log.Printf("event ACKed: %s", event.EventID)

		return nil
	}

	log.Printf("calling HandleEvent: %s", event.EventID)

	if err := handler.HandleEvent(event); err != nil {
		log.Printf("HandleEvent FAILED: %v", err)

		// Processing failed — ask RabbitMQ to redeliver.
		if nackErr := message.Nack(false, true); nackErr != nil {
			log.Printf("failed to nack message: %v", nackErr)
		}
		log.Println("🔥 consumer code changed")
		log.Println("🔥 consumer code changed")

		return err
	}

	log.Printf("HandleEvent succeeded: %s", event.EventID)

	log.Printf("calling MarkEventProcessed: %s", event.EventID)

	if err := storage.MarkEventProcessed(
		ctx,
		c.db,
		event.EventID,
	); err != nil {
		log.Printf("MarkEventProcessed FAILED: %v", err)

		// We successfully processed the event, but couldn't
		// record that fact. Don't ACK — redelivery is safer.
		if nackErr := message.Nack(false, true); nackErr != nil {
			log.Printf("failed to nack message: %v", nackErr)
		}

		return err
	}

	log.Printf("MarkEventProcessed succeeded: %s", event.EventID)

	if err := message.Ack(false); err != nil {
		return err
	}

	log.Printf("event ACKed: %s", event.EventID)

	return nil
}