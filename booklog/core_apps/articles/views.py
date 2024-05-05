from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .exceptions import DuplicateRecommendArticle
from .models import Article, ArticleView, Recommend
from .permissions import IsOwnerOrReadOnly
from .serializers import ArticleSerializer, RecommendSerializer

User = get_user_model()


# TODO: pagination, filter
class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = [
        "created_at",
        "updated_at",
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        # TODO: create a new article logging


class ArticleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "article_id"

    def get_object(self):
        article_id = self.kwargs.get("article_id")
        obj = get_object_or_404(Article, id=article_id)
        return obj

    def perform_update(self, instance):
        instance.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        viewer_ip = request.META.get("REMOTE_ADDR", None)
        ArticleView.record_view(article=instance, user=request.user, viewer_ip=viewer_ip)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        instance.delete()
        # TODO: delete instance logging


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
                "detail": "recommend added to article",
            },
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, *args, **kwargs):
        user = request.user
        article_id = kwargs.get("article_id")
        article = get_object_or_404(Article, id=article_id)

        clap = get_object_or_404(Recommend, user=user, article=article)
        clap.delete()
        return Response(
            {"detail": "Recommend cancel from article"},
            status=status.HTTP_204_NO_CONTENT,
        )
