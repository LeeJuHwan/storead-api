from .base import *  # noqa
from .base import env


SECRET_KEY = env("SIGNING_KEY")

DEBUG = env.bool("DJANGO_DEBUG", False)

CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]

ALLOWED_HOSTS = ['*']

DOMAIN = env("DOMAIN")
SITE_NAME = "Booklog for developers"
