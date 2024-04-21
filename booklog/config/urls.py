from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path(f"{settings.ADMIN_URL}", admin.site.urls),
    path("api/v1/auth/", include("core_apps.social_users.urls")),
    path("api/v1/articles/", include("core_apps.articles.urls")),
    path("api/v1/books/", include("core_apps.books.urls")),
    path("api/v1/profiles/", include("core_apps.profiles.urls")),
]


admin.site.site_header = "Storead API Admin"
admin.site.site_title = "Storead API Admin Portal"
admin.site.index_title = "Welcome to Storead API Portal"
