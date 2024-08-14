from django.urls import path

from core_apps.articles import views

urlpatterns = [
    path("", views.ArticleListCreateView.as_view(), name="article-list-search-create"),
    path(
        "/<uuid:article_id>",
        views.ArticleDetailAPI.as_view(),
        name="article-retrieve-upate-destory",
    ),
    path(
        "/<uuid:article_id>/recommend",
        views.RecommendArticleView.as_view(),
        name="article-recommend",
    ),
    path("/me", views.MyArticleDetailAPI.as_view(), name="my-article-detail"),
    path("/me/recommend", views.MyRecommendArticleAPI.as_view(), name="my-recommend-article-detail"),
]
