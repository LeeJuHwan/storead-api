from django.urls import path

from . import views

urlpatterns = [
    path(
        "rate_article/<uuid:article_id>/",
        views.RatingCreateView.as_view(),
        name="rating-create",
    ),
    path(
        "rate_article/<uuid:article_id>/update/",
        views.RatingUpdateView.as_view(),
        name="rating-update",
    ),
]
