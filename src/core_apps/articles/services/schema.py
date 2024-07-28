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
