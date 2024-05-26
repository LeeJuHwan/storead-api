from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from ..books.serializers import BookListSerializer
from .documents import ArticleDocument


class ArticleElasticSearchSerializer(DocumentSerializer):
    book = BookListSerializer(read_only=True)

    class Meta:
        document = ArticleDocument
        fields = ["title", "author_username", "book_title", "slug", "description", "body", "created_at"]
