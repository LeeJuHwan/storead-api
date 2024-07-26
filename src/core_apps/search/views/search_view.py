from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Serializer

from core_apps.articles.models import Article
from core_apps.articles.serializers import ArticleSerializer
from core_apps.shared.apis import BaseListAPIView
from core_apps.shared.swaggers import CommonRenderResponse, result_serializer


class SearchAPIView(BaseListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    @staticmethod
    def render_response(many=False):
        class ArticleRenderResponse(CommonRenderResponse):
            results = result_serializer(obj=ArticleSerializer(many=many), component_name="article")

        return ArticleRenderResponse()

    @extend_schema(
        summary="게시글 검색 API",
        tags=["게시글"],
        parameters=[
            OpenApiParameter(name="q", description="게시글 검색 키워드", required=False, type=OpenApiTypes.STR),
        ],
        responses=render_response(many=True),
    )
    def get(self, request, *args, **kwargs):
        """
        PostgreSQL FTS by pg_bigm extensions -> explain to bitmap heap scan
        """
        search_query = request.query_params.get("q")

        if not search_query:
            return self.list(request, *args, **kwargs)

        queryset = Article.objects.filter(title__contains=search_query)

        page: Response = self.paginate_queryset(queryset)
        serializer: Serializer | ModelSerializer = self.get_serializer(page, many=True)
        pagenated_response: Response = self.get_paginated_response(serializer.data)
        return self.success_response(data=pagenated_response.data, status_code=status.HTTP_200_OK)
