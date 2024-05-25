SPECTACULAR_SETTINGS = {
    "TITLE": "Storead",
    "DESCRIPTION": "서적을 읽고 정리 하는 공간",
    "CONTACT": {"name": "이주환", "url": "https://github.com/LeeJuHwan/storead-api", "email": "tmjhlee@gmail.com"},
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
        "filter": True,
    },
    "LICENSE": {
        "name": "MIT License",
        "url": "https://github.com/LeeJuHwan/storead-api/blob/main/LICENSE",
    },
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "//unpkg.com/swagger-ui-dist@5.9.1",
}


def swagger_urls():
    from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView, SpectacularAPIView
    from django.urls import path

    return [
        path("api/schema", SpectacularAPIView.as_view(), name="schema"),
        path("docs/swagger", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
        path("docs/redoc", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    ]
