from typing import Callable, Dict, Optional, Tuple

from core_apps.books.models import Book
from core_apps.books.serializers import BookInputSerializer
from core_apps.books.services.book_query import BookQuery


class BookService:
    query = BookQuery()
    model = Book

    def get_book(self, book_id: str, id_type: str) -> Optional[Book]:
        """
        책 아이디 또는 ISBN을 기준으로 책 조회
        """

        types = {
            "isbn": self.query.get_book_by_isbn,
            "id": self.query.get_book_by_id,
        }

        select_query: Callable = types[id_type]

        return select_query(book_id)

    def get_or_create_book_by_isbn(self, isbn: str, data: Dict[str, str]) -> Tuple[Optional[Book], bool]:
        """
        책 정보 생성 시 등록 되어있다면 조회, 없다면 생성
        """
        book: Optional[Book] = None
        created: bool = False

        if isbn:
            book = self.get_book(isbn, id_type="isbn")

        if book is None:
            request = BookInputSerializer(data=data)
            request.is_valid(raise_exception=True)
            book = Book.objects.create(**request.validated_data)
            created = True

        return book, created
