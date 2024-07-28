from rest_framework import serializers

from core_apps.articles.serializers import ArticleSerializer, RecommendSerializer
from core_apps.shared.swaggers import CommonRenderResponse, result_serializer


class RecommendCreateOutputSchema(CommonRenderResponse):
    results = RecommendSerializer()


class ArticleOutputSchema(CommonRenderResponse):
    results = ArticleSerializer()


def article_render_response(many=False):
    class ArticleRenderResponse(CommonRenderResponse):
        results = result_serializer(obj=ArticleSerializer(many=many), component_name="article")

    return ArticleRenderResponse()


class ArticleCreateRenderRequest(serializers.Serializer):
    """
     "title": "title",
     "tags": ["tags1", "tags2"],
     "description": "description",
     "body": "body context",
    "book": "026ae117-2e41-4658-9fde-850f1462bee5"
    """

    title = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())
    description = serializers.CharField()
    body = serializers.CharField()
    book = serializers.UUIDField()
