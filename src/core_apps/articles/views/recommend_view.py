from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response

from core_apps.articles.exceptions import DuplicateRecommendArticle
from core_apps.articles.models import Article, Recommend
from core_apps.articles.serializers.article_serializer import RecommendSerializer
from core_apps.shared.swaggers import OutputSerializer, UuidSerializer


class RecommendArticleView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Recommend.objects.all()
    serializer_class = RecommendSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        article_id = kwargs.get("article_id")
        article = get_object_or_404(Article, id=article_id)

        if Recommend.objects.filter(user=user, article=article).exists():
            raise DuplicateRecommendArticle()

        recommend = Recommend.objects.create(user=user, article=article)
        recommend.save()
        return Response(
            {
                "message": "recommend added to article",
            },
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        summary="게시글 추천 API",
        tags=["게시글"],
        request=UuidSerializer,
        responses=OutputSerializer,
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @extend_schema(
        summary="게시글 추천 취소 API",
        tags=["게시글"],
        request=UuidSerializer,
        responses=OutputSerializer,
    )
    def delete(self, request, *args, **kwargs):
        user = request.user
        article_id = kwargs.get("article_id")
        article = get_object_or_404(Article, id=article_id)

        clap = get_object_or_404(Recommend, user=user, article=article)
        clap.delete()
        return Response(
            {"message": "Recommend cancel from article"},
            status=status.HTTP_204_NO_CONTENT,
        )
