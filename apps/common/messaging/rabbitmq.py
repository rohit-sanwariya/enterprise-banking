import json

import pika
from django.conf import settings

from .events import Event


def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(
        settings.RABBITMQ_USER,
        settings.RABBITMQ_PASSWORD,
    )

    parameters = pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        credentials=credentials,
    )

    return pika.BlockingConnection(parameters)


def declare_exchange(connection):
    channel = connection.channel()

    channel.exchange_declare(
        exchange="banking.events",
        exchange_type="topic",
        durable=True,
    )


def declare_notification_queue(connection):
    channel = connection.channel()

    channel.queue_declare(
        queue="notifications",
        durable=True,
    )


def bind_notification_queue(connection):
    channel = connection.channel()

    channel.queue_bind(
        exchange="banking.events",
        queue="notifications",
        routing_key="account.*",
    )


def publish_event(connection, event: Event):
    channel = connection.channel()

    channel.basic_publish(
        exchange="banking.events",
        routing_key=event.event_type,
        body=json.dumps(
            {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "occurred_at": event.occurred_at.isoformat(),
                "data": event.data,
            }
        ),
    )
