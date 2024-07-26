from rest_framework import serializers

from core_apps.books.models import Book


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
