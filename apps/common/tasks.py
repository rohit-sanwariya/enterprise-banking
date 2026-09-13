from celery import shared_task

from apps.common.messaging.EventPublisher import EventPublisher
from apps.common.messaging.events import Event
from apps.common.models import OutboxEvent


@shared_task
def publish_outbox_events():
    events = OutboxEvent.objects.filter(published=False).order_by("created_at")[:100]

    for outbox_event in events:
        event = Event(
            event_id=str(outbox_event.id),
            event_type=outbox_event.event_type,
            occurred_at=outbox_event.created_at,
            data=outbox_event.payload,
        )

        EventPublisher.publish(event)

        outbox_event.published = True
        outbox_event.save(update_fields=["published"])
