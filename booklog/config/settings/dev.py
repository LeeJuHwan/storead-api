from .base import *  # noqa
from .base import env

DEBUG = env.bool("DJANGO_DEBUG", False)

CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]

ALLOWED_HOSTS = ["*"]

DOMAIN = env.str("DOMAIN", "")
SITE_NAME = "Booklog for developers"

CORS_ALLOW_ALL_ORIGINS: True
