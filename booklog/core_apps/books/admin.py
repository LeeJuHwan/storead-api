from django.contrib import admin

from .models import Book


class BookAdmin(admin.ModelAdmin):
    ordering = ["-created_at"]
    model = Book

    list_display = [
        "pkid",
        "isbn",
        "title",
        "author",
        "published_date",
    ]

    list_display_links = ["pkid", "isbn", "title", "author"]

    list_filter = [
        "pkid",
        "title",
        "created_at",
    ]

    search_fields = ["title", "author", "isbn"]


admin.site.register(Book, BookAdmin)
