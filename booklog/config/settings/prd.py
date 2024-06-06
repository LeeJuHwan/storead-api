from .base import env  # noqa

DEBUG = env.ENV.bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS = ["*"]

SITE_NAME = "Storead"

CORS_ALLOW_ALL_ORIGINS: True

DATABASES = {"default": env.ENV.db("DATABASE_URL")}
