from django.urls import path

from . import views

urlpatterns = [
    path("", views.ArticleListCreateView.as_view(), name="article-list-create"),
    path(
        "/<uuid:article_id>",
        views.ArticleRetrieveUpdateDestroyView.as_view(),
        name="article-retrieve-upate-destory",
    ),
    path(
        "/<uuid:article_id>/recommend",
        views.RecommendArticleView.as_view(),
        name="article-recommend",
    ),
]
