from django.urls import path

from . import views

urlpatterns = [
    path("", views.BookListAPIView.as_view(), name="book-list"),
    path("/<uuid:book_id>", views.BookDetailAPIView.as_view(), name="book-detail"),
]
