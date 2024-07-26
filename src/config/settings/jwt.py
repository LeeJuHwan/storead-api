from datetime import timedelta

from config.env import ENV

REST_AUTH = {
    "SESSION_LOGIN": False,
    "USE_JWT": True,
    "JWT_AUTH_HTTPONLY": True,
    "JWT_AUTH_COOKIE": "access-token",
    "JWT_AUTH_REFRESH_COOKIE": "refresh-token",
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "SIGNING_KEY": ENV.str("SECRET_KEY", default="dev"),
    "USER_ID_FIELD": "uuid",
    "USER_ID_CLAIM": "user_id",
}
