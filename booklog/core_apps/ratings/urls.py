from django.urls import path

from . import views

urlpatterns = [
    path("/rate_article/<uuid:article_id>", views.RatingAPIView.as_view(), name="rating-create-update"),
]
