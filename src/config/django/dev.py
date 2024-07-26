from .base import *  # noqa

DEBUG = env.ENV.bool("DJANGO_DEBUG", False)

CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]

ALLOWED_HOSTS = ["*"]

CORS_ALLOW_ALL_ORIGINS: True

DATABASES = {"default": env.ENV.db("DATABASE_URL")}
