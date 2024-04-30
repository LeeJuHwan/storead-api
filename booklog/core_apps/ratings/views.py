from core_apps.articles.models import Article
from core_apps.ratings.exceptions import (
    ArticleIdNotFound,
    OnlyAuthorRated,
    YouDontHaveRated,
    YouhaveAlreadyRated,
)
from rest_framework import generics

from .models import Rating
from .permissions import IsOwnerOrReadOnly
from .serializers import RatingSerializer


class RatingArticleSelector:
    def get_article(self, article_id):
        if article_id:
            try:
                # NOTE: 작성자만 본인이 읽은 책에 대한 평점만 입력 할 수 있다
                return Article.objects.get(author=self.request.user, id=article_id)
            except Article.DoesNotExist:
                raise OnlyAuthorRated
        raise ArticleIdNotFound


class RatingCreateView(generics.CreateAPIView, RatingArticleSelector):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        article = self.get_article(self.kwargs.get("article_id"))
        user = self.request.user

        if Rating.objects.filter(user=user, article=article).exists():
            raise YouhaveAlreadyRated

        serializer.save(user=self.request.user, article=article)


class RatingUpdateView(generics.UpdateAPIView, RatingArticleSelector):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Rating.objects.select_related("article")

    def get_object(self):
        article_id = self.kwargs.get("article_id")
        user = self.request.user
        return self.get_queryset().get(user=user, article__id=article_id)

    def perform_update(self, serializer):
        article = self.get_article(self.kwargs.get("article_id"))
        user = self.request.user

        rating = Rating.objects.filter(user=user, article=article).first()
        if not rating:
            raise YouDontHaveRated

        serializer.save(user=user, article=article)
