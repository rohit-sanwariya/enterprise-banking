from apps.common.messaging.events import Event
from apps.common.messaging.rabbitmq import get_rabbitmq_connection, publish_event


class EventPublisher:
    @staticmethod
    def publish(event: Event):
        connection = get_rabbitmq_connection()
        try:
            publish_event(connection, event)
        finally:
            connection.close()
