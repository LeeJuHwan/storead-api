from .models import Book


class BookSelector:
    model = Book

    def get_book_by_id(self, book_id: str):
        try:
            book = self.model.objects.get(id=book_id)
        except Book.DoesNotExist:
            book = None

        return book

    def get_book_by_isbn(self, isbn: str):
        try:
            book = Book.objects.get(isbn=isbn)
        except Book.DoesNotExist:
            book = None

        return book
