# config/settings/local.py

import environ

from .base import *

# Initialize environ
env = environ.Env()

# Read .env file from repository root
env.read_env(BASE_DIR / ".env")

# Local development settings
SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
]

# Database configuration
DATABASES = {
    "default": env.db(),
}

# Logging
#
# Keep Django/framework logging at INFO so that DEBUG-level
# file/import noise from .venv is not printed.
#
# Keep our application logs at DEBUG so we can still debug
# business/domain/application code.

LOGGING["root"]["level"] = "INFO"
LOGGING["root"]["handlers"] = ["console", "file"]

LOGGING["loggers"]["django"]["level"] = "INFO"
LOGGING["loggers"]["django"]["handlers"] = ["console", "file"]

LOGGING["loggers"]["apps"]["level"] = "DEBUG"
LOGGING["loggers"]["apps"]["handlers"] = ["console", "file"]
SHELL_PLUS_IMPORTS = [
    "from apps.common.messaging.rabbitmq import get_rabbitmq_connection,declare_exchange,declare_notification_queue,bind_notification_queue",
]
print("=== local.py loaded successfully ===")
RABBITMQ_HOST = env("RABBITMQ_HOST")
RABBITMQ_PORT = env.int("RABBITMQ_PORT")
RABBITMQ_USER = env("RABBITMQ_USER")
RABBITMQ_PASSWORD = env("RABBITMQ_PASSWORD")


CELERY_BROKER_URL = (
    f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}//"
)
CELERY_BEAT_SCHEDULE = {
    "publish-outbox-events": {
        "task": "apps.common.tasks.publish_outbox_events",
        "schedule": 5.0,
    },
}
CELERY_CONTROL_QUEUE_EXCLUSIVE = True
CELERY_EVENT_QUEUE_EXCLUSIVE = True
