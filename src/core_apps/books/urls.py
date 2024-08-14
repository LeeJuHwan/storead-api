from django.urls import path

from core_apps.books.views import book_view as views

urlpatterns = [
    path("", views.BookListAPI.as_view(), name="book-list"),
    path("/<uuid:book_id>", views.BookDetailAPI.as_view(), name="book-detail"),
]
