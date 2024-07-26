from .base import *  # noqa
from .base import env

DEBUG = env.ENV.bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS = ["api.storead.site"]

SITE_NAME = "Storead"

DATABASES = {"default": env.ENV.db("DATABASE_URL")}
