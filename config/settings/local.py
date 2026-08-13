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

print("=== local.py loaded successfully ===")
