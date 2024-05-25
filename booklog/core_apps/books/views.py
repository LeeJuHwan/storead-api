"""
    전체 사용자가 등록한 책 정보 관리
"""

import uuid

from core_apps.common.paginations import CommonCursorPagination
from core_apps.common.swaggers import UuidSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book
from .queries import BookSelector
from .serializers import BookListSerializer


class BookListAPIView(ListCreateAPIView):
    model = Book
    serializer_class = BookListSerializer
    permission_classes = [AllowAny]
    pagination_class = CommonCursorPagination
    queryset = Book.objects.all()
    selector = BookSelector()
    ordering_fields = ["created_at"]

    class RequestSerializer(serializers.Serializer):
        isbn = serializers.CharField()
        description = serializers.CharField()
        title = serializers.CharField()
        author = serializers.CharField()
        published_date = serializers.CharField()
        thumbnail_url = serializers.ImageField()

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
    def post(self, request, *args, **kwargs):
        isbn = request.data.get("isbn")
        created = False

        if isbn:
            book = self.selector.get_book_by_isbn(isbn)

        if book is None:
            serializer = self.RequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            book, created = Book.objects.get_or_create(isbn=isbn)

        serializer = self.ResponseSerializer(book)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK

        return Response(serializer.data, status=status_code)


class BookDetailAPIView(APIView):
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
            return NotFound("can't find book")

        serializer_data = self.BookDetailResponse(book).data
        return Response(serializer_data, status=status.HTTP_200_OK)
