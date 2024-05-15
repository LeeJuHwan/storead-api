from django.urls import path

from .views import CommentListCreateView, CommentUpdateDeleteView

urlpatterns = [
    path(
        "/article/<uuid:article_id>",
        CommentListCreateView.as_view(),
        name="article_comments",
    ),
    path("/<uuid:id>", CommentUpdateDeleteView.as_view(), name="comment_detail"),
]
