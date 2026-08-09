from .local import *

# Use the same env-based database configuration as the local settings.
# This ensures pytest loads a valid DATABASES setting from .env.

# If .env is missing in test environments, django-environ will raise a clear error.
