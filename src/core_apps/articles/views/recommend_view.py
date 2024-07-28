from drf_spectacular.utils import extend_schema
from rest_framework import status

from core_apps.articles.serializers import schema
from core_apps.articles.serializers.article_serializer import RecommendSerializer
from core_apps.articles.services.recommend_service import RecommendService
from core_apps.shared.apis import BaseAPIView
from core_apps.shared.swaggers import DeleteOutputSchema, UuidSerializer


class RecommendArticleView(BaseAPIView):
    service = RecommendService()

    @extend_schema(
        summary="게시글 추천 API",
        tags=["추천"],
        request=UuidSerializer,
        responses=schema.RecommendCreateOutputSchema(),
    )
    def post(self, request, article_id, *args, **kwargs):
        recommend = self.service.create_recommend(request.user, article_id)
        output_serializer = RecommendSerializer(recommend)
        return self.success_response(
            output_serializer.data, message="successfully recommend on article", status_code=status.HTTP_201_CREATED
        )

    @extend_schema(
        summary="게시글 추천 취소 API",
        tags=["추천"],
        request=UuidSerializer,
        responses={200: DeleteOutputSchema()},
    )
    def delete(self, request, article_id, *args, **kwargs):
        user = request.user

        self.service.delete_recommend(user, article_id)
        return self.success_response(message="Recommend cancel from article", status_code=status.HTTP_200_OK)
