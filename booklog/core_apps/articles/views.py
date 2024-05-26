from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, generics, permissions, serializers, status
from rest_framework.response import Response

from ..common.paginations import CommonCursorPagination
from ..common.swaggers import OutputSerializer, UuidSerializer
from .exceptions import DuplicateRecommendArticle
from .filters import ArticleFilter
from .models import Article, ArticleView, Recommend
from .permissions import IsOwnerOrReadOnly
from .serializers import ArticleSerializer, RecommendSerializer

User = get_user_model()


class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = CommonCursorPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = ArticleFilter
    ordering_fields = [
        "created_at",
        "updated_at",
    ]

    class RequestArticleList(serializers.Serializer):
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

    def get_permissions(self):
        permission_options = {
            "GET": [permissions.AllowAny()],
            "POST": [permissions.IsAuthenticated()],
        }
        permission = permission_options.get(self.request.method)

        if not permission:
            return [permissions.IsAuthenticated()]
        return permission

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @extend_schema(
        summary="게시글 목록 조회 API",
        tags=["게시글"],
        responses=ArticleSerializer(many=True),
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary="게시글 생성 API",
        tags=["게시글"],
        request=RequestArticleList,
        responses=ArticleSerializer(many=True),
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ArticleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "article_id"

    def get_object(self):
        article_id = self.kwargs.get("article_id")
        obj = get_object_or_404(Article, id=article_id)
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        viewer_ip = request.META.get("REMOTE_ADDR", None)
        ArticleView.record_view(article=instance, user=request.user, viewer_ip=viewer_ip)
        return Response(serializer.data)

    @extend_schema(
        summary="게시글 수정 API",
        tags=["게시글"],
        responses=ArticleSerializer(many=True),
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="상세 게시글 조회 API",
        tags=["게시글"],
        request=UuidSerializer,
        responses=ArticleSerializer(many=True),
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="게시글 삭제 API",
        tags=["게시글"],
        request=UuidSerializer,
        responses=ArticleSerializer(many=True),
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


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
