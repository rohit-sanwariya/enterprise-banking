package messaging

import (
	"github.com/rabbitmq/amqp091-go"
)

const (
	ExchangeName = "banking.events"
	QueueName    = "notifications"
	RoutingKey   = "account.*"
)

func Connect(url string) (*amqp091.Connection, *amqp091.Channel, error) {
	conn, err := amqp091.Dial(url)
	if err != nil {
		return nil, nil, err
	}

	ch, err := conn.Channel()
	if err != nil {
		conn.Close()
		return nil, nil, err
	}

	return conn, ch, nil
}

func Setup(ch *amqp091.Channel) error {
	err := ch.ExchangeDeclare(
		ExchangeName,
		"topic",
		true,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		return err
	}

	_, err = ch.QueueDeclare(
		QueueName,
		true,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		return err
	}

	return ch.QueueBind(
		QueueName,
		RoutingKey,
		ExchangeName,
		false,
		nil,
	)
}