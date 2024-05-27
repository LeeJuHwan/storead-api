from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from drf_spectacular.utils import extend_schema
from rest_framework import permissions

from .docs import ordering_parameter, search_parameter
from .documents import ArticleDocument
from .serializers import ArticleElasticSearchSerializer


class ArticleElasticSearchView(DocumentViewSet):
    document = ArticleDocument
    serializer_class = ArticleElasticSearchSerializer
    lookup_field = "id"
    permission_classes = [permissions.AllowAny]

    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]

    search_fields = (
        "title",
        "book_title",
        "description",
        "body",
        "author_username",
        "tags",
    )
    filter_fields = {
        "slug": "slug.raw",
        "tags": "tags",
        "created_at": "created_at",
    }

    ordering_fields = {
        "created_at": "created_at",
    }
    ordering = ("-created_at",)

    @extend_schema(
        summary="게시글 검색 API",
        tags=["검색"],
        parameters=[search_parameter, ordering_parameter],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
