from core_apps.articles.queries import ArticleSelector
from rest_framework import status, views
from rest_framework.response import Response

from .permissions import IsOwnerOrReadOnly
from .queries import RatingSelector
from .serializers import RatingSerializer


class RatingAPIView(views.APIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer = RatingSerializer
    selector = RatingSelector()

    def _get_article(self, user, article_id):
        selector = ArticleSelector()  # NOTE: Singleton instance to reusing
        return selector.get_article(user, article_id)

    def _validate_user_rating(self, func, *args):
        func(*args)

    def post(self, request, *args, **kwargs):
        user = request.user
        article_id = kwargs.get("article_id")
        article = self._get_article(user, article_id)
        self._validate_user_rating(self.selector.get_exists_rate_on_article, user, article_id)

        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, article=article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        user = request.user
        article_id = kwargs.get("article_id")
        rating = self.selector.get_rating_select_related(user, article_id)
        article = self._get_article(user, article_id)
        self._validate_user_rating(self.selector.get_not_exists_rate_on_article, user, article_id)

        serializer = RatingSerializer(rating, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, article=article)
        return Response(serializer.data, status=status.HTTP_200_OK)
