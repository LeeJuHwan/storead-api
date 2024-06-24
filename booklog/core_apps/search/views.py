from django_elasticsearch_dsl_drf.constants import (
    FUNCTIONAL_SUGGESTER_COMPLETION_MATCH,
    FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
    SUGGESTER_COMPLETION,
    SUGGESTER_TERM,
)
from django_elasticsearch_dsl_drf.filter_backends import (  # SearchFilterBackend,
    CompoundSearchFilterBackend,
    DefaultOrderingFilterBackend,
    FilteringFilterBackend,
    FunctionalSuggesterFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .docs import (
    auto_suggest_response,
    ordering_parameter,
    search_parameter,
    suggest_parameter,
)
from .documents import ArticleDocument
from .serializers import ArticleElasticSearchSerializer


class ArticleElasticSearchView(DocumentViewSet):
    document = ArticleDocument
    serializer_class = ArticleElasticSearchSerializer
    lookup_field = "id"
    permission_classes = [permissions.AllowAny]

    filter_backends = [
        SuggesterFilterBackend,
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        # SearchFilterBackend,
        CompoundSearchFilterBackend,
        FunctionalSuggesterFilterBackend,
    ]

    suggester_fields = {
        "title": {
            "field": "title.suggest",
            "suggesters": [
                SUGGESTER_COMPLETION,
                SUGGESTER_TERM,
            ],
            "options": {
                "fuzzy": {
                    "fuzziness": 1,
                }
            },
        },
    }

    # Functional suggester fields
    functional_suggester_fields = {
        "title": {
            "field": "title.suggest",
            "suggesters": [
                FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
            ],
            "default_suggester": FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
            "options": {
                "size": 25,
                "from": 0,
            },
        },
        "title_match": {
            "field": "title.edge_ngram_completion",
            "suggesters": [FUNCTIONAL_SUGGESTER_COMPLETION_MATCH],
            "default_suggester": FUNCTIONAL_SUGGESTER_COMPLETION_MATCH,
        },
    }

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

    @extend_schema(
        summary="제목 자동완성 API",
        tags=["검색"],
        parameters=[suggest_parameter, ordering_parameter],
        examples=[auto_suggest_response],
    )
    @action(detail=False)
    def suggest(self, request):
        """Suggest functionality."""
        queryset = self.filter_queryset(self.get_queryset())
        is_suggest = getattr(queryset, "_suggest", False)
        if not is_suggest:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        page = self.paginate_queryset(queryset)
        return Response(page)
