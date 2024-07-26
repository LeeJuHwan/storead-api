from django.urls import path

from core_apps.search.views import search_view as views

urlpatterns = [
    path("", views.SearchAPIView.as_view(), name="article-search"),
]
