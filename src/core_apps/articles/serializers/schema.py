from rest_framework import serializers


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
