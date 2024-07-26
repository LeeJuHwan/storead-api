from config import env

SECRET_KEY = env.ENV("SIGNING_KEY", default="0_w4ttc_r+95i0c^4v2ea7ppol817er--ef!&&s2c41r&g3cdy")

SOCIAL_PLATFORM = env.load_yaml_file(env.super_secret_yaml).get("social")
PLATFORM_URL = env.load_yaml_file(env.super_secret_yaml).get("platform_url")

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "taggit",
    "drf_spectacular",
    "django_filters",
    "storages",
]

LOCAL_APPS = [
    "core_apps.social_users",
    "core_apps.articles",
    "core_apps.books",
    "core_apps.profiles",
    "core_apps.comments",
    "core_apps.ratings",
    "core_apps.search",
]

INSTALLED_APPS = [
    *DJANGO_APPS,
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "config.settings.middleware.RequestLoggingMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.core_urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": env.ROOT_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


AUTHENTICATION_BACKENDS = ["core_apps.social_users.admin.AdminAuthBackend"]


LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = False

SITE_ID = 1

ADMIN_URL = "superadmin/"

AUTH_USER_MODEL = "social_users.SocialUser"

APPEND_SLASH = False


STATIC_URL = "/staticfiles/"
STATIC_ROOT = str(env.ROOT_DIR.parent / "staticfiles")

MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = str(env.ROOT_DIR.parent / "mediafiles")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

from config.settings.jwt import *  # noqa
from config.settings.rest_framework import *  # noqa
from config.settings.logging import *  # noqa
from config.settings.sentry import *  # noqa
from config.settings.swagger import *  # noqa
from config.settings.storages import *  # noqa
