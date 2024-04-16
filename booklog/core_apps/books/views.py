"""
    전체 사용자가 등록한 정보 목록 불러오기
"""

from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .models import Book
from .serializers import BookListSerializer


# TODO: Pagination을 통해 API 성능 향상
# TODO: 미디어파일 endpoint 제공
class BookListAPIView(ListAPIView):
    model = Book
    serializer_class = BookListSerializer
    permission_classes = [AllowAny]
    queryset = Book.objects.all()
