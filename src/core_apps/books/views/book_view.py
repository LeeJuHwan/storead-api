"""
    전체 사용자가 등록한 책 정보 관리
"""

import uuid
from typing import Optional

from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from core_apps.books.models import Book
from core_apps.books.serializers import (
    BookInputSerializer,
    BookListSerializer,
    BookOutputSerializer,
)
from core_apps.books.services.book_service import BookService
from core_apps.shared import apis
from core_apps.shared.swaggers import UuidSerializer


class BookListAPIView(apis.BaseListAPIView):
    model = Book
    serializer_class = BookListSerializer
    permission_classes = [AllowAny]
    queryset = Book.objects.all()
    ordering_fields = ["created_at"]
    service = BookService()

    @extend_schema(
        summary="책 목록 조회 API",
        tags=["책"],
        responses=BookOutputSerializer(many=True),
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary="책 등록 API",
        tags=["책"],
        request=BookInputSerializer(),
        responses=BookOutputSerializer(),
    )
    def post(self, request: Request, *args, **kwargs):
        book: Optional[Book]
        created: bool

        isbn: str = request.data.get("isbn")
        book, created = self.service.get_or_create_book_by_isbn(isbn, request.data)

        output_serializer = BookOutputSerializer(book)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return self.success_response(output_serializer.data, status_code=status_code)


class BookDetailAPIView(apis.BaseAPIView):
    permission_classes = [AllowAny]
    service = BookService()

    class BookDetailResponse(serializers.Serializer):
        id = serializers.UUIDField()
        isbn = serializers.CharField()
        title = serializers.CharField()
        author = serializers.CharField()
        published_date = serializers.CharField()
        description = serializers.CharField()
        thumbnail_url = serializers.ImageField()

    @extend_schema(
        summary="책 상세 정보 조회 API",
        tags=["책"],
        request=UuidSerializer,
        responses={status.HTTP_200_OK: BookDetailResponse},
    )
    def get(self, request: Request, book_id: uuid) -> Response:
        book: Book = self.service.get_book(book_id, id_type="id")

        if not book:
            return self.fail_response("can't find the book")

        serializer_data = self.BookDetailResponse(book).data
        return self.success_response(serializer_data, status_code=status.HTTP_200_OK)
