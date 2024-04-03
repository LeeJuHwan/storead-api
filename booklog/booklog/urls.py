from django.contrib import admin
from django.urls import path
from django.conf import settings


urlpatterns = [
    path(f"{settings.ADMIN_URL}", admin.site.urls),
]


admin.site.site_header = "Booklog API Admin"

admin.site.site_title = "Booklog API Admin Portal"

admin.site.index_title = "Welcome to Booklog API Portal"
