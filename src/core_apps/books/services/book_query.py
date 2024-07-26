from core_apps.books.models import Book


class BookQuery:
    model = Book

    def get_book_by_id(self, book_id: str):
        try:
            book = self.model.objects.get(id=book_id)
        except self.model.DoesNotExist:
            book = None

        return book

    def get_book_by_isbn(self, isbn: str):
        try:
            book = self.model.objects.get(isbn=isbn)
        except self.model.DoesNotExist:
            book = None

        return book
