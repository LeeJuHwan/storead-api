from django.urls import path

from core_apps.comments.views import comment_view as views

urlpatterns = [
    path(
        "/article/<uuid:article_id>",
        views.CommentListCreateView.as_view(),
        name="article_comments",
    ),
    path("/<uuid:comment_id>", views.CommentUpdateDeleteView.as_view(), name="comment_detail"),
]
