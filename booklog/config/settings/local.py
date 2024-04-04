from .base import *  # noqa
# from .base import env


# SECRET_KEY = env(
#     "DJANGO_SECRET_KEY",
#     default="oXPWQPA3C3sdBCuBeXUKq3LBp9YDJ33-306p9EAKf1ja1xkWnKY",
# )


DEBUG = True

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080", "http://127.0.0.1:8080"]


# DOMAIN = env("DOMAIN")
SITE_NAME = "Booklog for developers"
