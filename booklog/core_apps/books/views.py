"""
    전체 사용자가 등록한 정보 목록 불러오기
"""

import uuid

from core_apps.common.paginations import CommonCursorPagination
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .docs import BookDetailDocument
from .models import Book
from .queries import BookSelector
from .serializers import BookListSerializer


class BookListAPIView(ListCreateAPIView):
    model = Book
    serializer_class = BookListSerializer
    permission_classes = [AllowAny]
    pagination_class = CommonCursorPagination
    queryset = Book.objects.all()
    ordering_fields = ["created_at"]


class BookDetailAPIView(APIView):
    serializer_class = BookListSerializer
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    selector = BookSelector()

    class ResponseSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        isbn = serializers.CharField()
        title = serializers.CharField()
        author = serializers.CharField()
        published_date = serializers.DateField()
        description = serializers.CharField()
        thumbnail_url = serializers.ImageField()

    @BookDetailDocument(
        request_serializer=serializers.UUIDField(),
        response_serializer=ResponseSerializer,
    )
    def get(self, request: Request, book_id: uuid) -> Response:
        book = self.selector.get_book_by_id(book_id)

        if not book:
            return NotFound("can't find book")

        serializer = self.ResponseSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
