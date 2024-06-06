from .base import *  # noqa

DEBUG = env.ENV.bool("DJANGO_DEBUG", False)

CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]

ALLOWED_HOSTS = ["*"]

SITE_NAME = "Booklog for developers"

CORS_ALLOW_ALL_ORIGINS: True
