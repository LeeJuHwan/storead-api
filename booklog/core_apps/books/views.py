"""
    전체 사용자가 등록한 책 정보 관리
"""

import uuid
from typing import Optional

from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status

# from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..common import apis
from ..common.swaggers import UuidSerializer
from .models import Book
from .queries import BookSelector
from .serializers import BookListSerializer


class BookListAPIView(apis.BaseListAPIView):
    model = Book
    serializer_class = BookListSerializer
    permission_classes = [AllowAny]
    queryset = Book.objects.all()
    selector = BookSelector()
    ordering_fields = ["created_at"]

    class RequestSerializer(serializers.Serializer):
        isbn = serializers.CharField()
        description = serializers.CharField()
        title = serializers.CharField()
        author = serializers.CharField()
        published_date = serializers.CharField()
        thumbnail_url = serializers.ImageField(required=False)

    class ResponseSerializer(serializers.Serializer):
        pkid = serializers.IntegerField()
        id = serializers.UUIDField()
        created_at = serializers.CharField()
        isbn = serializers.CharField()
        title = serializers.CharField()
        author = serializers.CharField()
        published_date = serializers.CharField()
        description = serializers.CharField()
        thumbnail_url = serializers.ImageField()

    @extend_schema(
        summary="책 목록 조회 API",
        tags=["책"],
        responses=ResponseSerializer(many=True),
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary="책 등록 API",
        tags=["책"],
        request=RequestSerializer,
        responses=ResponseSerializer,
    )
    def post(self, request: Request, *args, **kwargs):
        isbn: str = request.data.get("isbn")
        created: bool = False
        book: Optional[Book] = None

        if isbn:
            book: Book = self.selector.get_book_by_isbn(isbn)

        if book is None:
            request = self.RequestSerializer(data=request.data)
            request.is_valid(raise_exception=True)
            book = Book.objects.create(**request.validated_data)
            created = True

        response = self.ResponseSerializer(book)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK

        return self.success_response(response.data, status_code=status_code)


class BookDetailAPIView(apis.BaseAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    selector = BookSelector()

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
        book = self.selector.get_book_by_id(book_id)

        if not book:
            return self.fail_response("can't find the book")

        serializer_data = self.BookDetailResponse(book).data
        return self.success_response(serializer_data, status_code=status.HTTP_200_OK)
