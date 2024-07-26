from drf_spectacular.utils import extend_schema
from rest_framework import status

from core_apps.ratings.permissions import IsOwnerOrReadOnly
from core_apps.ratings.serializers import RatingSerializer
from core_apps.ratings.services.rating_service import RatingService
from core_apps.shared.apis import BaseAPIView


class RatingAPIView(BaseAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer = RatingSerializer
    service = RatingService()

    @extend_schema(
        summary="평점 등록 API",
        tags=["평점"],
        request=RatingSerializer,
        responses=RatingSerializer,
    )
    def post(self, request, article_id):
        user = request.user

        input_serializer = self.serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        rating = self.service.create_rating(article_id, user, input_serializer.validated_data)

        output_serializer = RatingSerializer(rating)
        return self.success_response(
            data=output_serializer.data, message="successfully rate on article", status_code=status.HTTP_201_CREATED
        )

    @extend_schema(
        summary="평점 수정 API",
        tags=["평점"],
        request=RatingSerializer,
        responses=RatingSerializer,
    )
    def put(self, request, article_id):
        user = request.user
        rating = self.service.update_rating(article_id, user, request.data)
        output_serializer = RatingSerializer(rating)
        return self.success_response(output_serializer.data, message="successfully updated!")
