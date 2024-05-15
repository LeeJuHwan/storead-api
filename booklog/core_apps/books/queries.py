from .models import Book


class BookSelector:
    model = Book

    def get_book_by_id(self, book_id):
        try:
            return self.model.objects.get(id=book_id)
        except Book.DoesNotExist:
            return
