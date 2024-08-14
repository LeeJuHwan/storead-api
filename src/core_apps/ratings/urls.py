from django.urls import path

from core_apps.ratings import views

urlpatterns = [
    path("/rate_article/<uuid:article_id>", views.RatingAPI.as_view(), name="rating-create-update"),
]
