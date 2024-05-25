from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from .swagger import swagger_urls

urlpatterns = [
    path(f"{settings.ADMIN_URL}", admin.site.urls),
    path("api/v1/auth", include("core_apps.social_users.urls")),
    path("api/v1/articles", include("core_apps.articles.urls")),
    path("api/v1/books", include("core_apps.books.urls")),
    path("api/v1/profiles", include("core_apps.profiles.urls")),
    path("api/v1/comments", include("core_apps.comments.urls")),
    path("api/v1/ratings", include("core_apps.ratings.urls")),
]

if settings.DEBUG:
    urlpatterns.extend(swagger_urls())

admin.site.site_header = "Storead API Admin"
admin.site.site_title = "Storead API Admin Portal"
admin.site.index_title = "Welcome to Storead API Portal"
