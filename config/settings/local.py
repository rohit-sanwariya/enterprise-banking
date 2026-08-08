# config/settings/local.py
import environ

from .base import BASE_DIR, LOGGING

# Initialize environ
env = environ.Env()

# Read .env file from repository root
env.read_env(BASE_DIR / ".env")

# Override settings
SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# Database configuration
DATABASES = {"default": env.db()}

# More verbose logging for local development
LOGGING["root"]["level"] = "DEBUG"
LOGGING["loggers"]["django"]["level"] = "DEBUG"
LOGGING["loggers"]["apps"]["level"] = "DEBUG"
LOGGING["root"]["handlers"] = ["console", "file"]
LOGGING["loggers"]["django"]["handlers"] = ["console", "file"]
LOGGING["loggers"]["apps"]["handlers"] = ["console", "file"]

print("=== local.py loaded successfully ===")
