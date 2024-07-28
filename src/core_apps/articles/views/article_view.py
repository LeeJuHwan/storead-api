from django.contrib.auth import get_user_model
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import permissions, status

from core_apps.articles.models import Article, ArticleView
from core_apps.articles.permissions import IsOwnerOrReadOnly
from core_apps.articles.serializers import ArticleCreateRenderRequest, ArticleSerializer
from core_apps.articles.services import schema
from core_apps.articles.services.article_service import ArticleService
from core_apps.shared.apis import BaseAPIView, BaseListAPIView
from core_apps.shared.paginations import CommonCursorPagination
from core_apps.shared.swaggers import DeleteOutputSchema, UuidSerializer

User = get_user_model()


class ArticleListCreateView(BaseListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = CommonCursorPagination
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = [
        "created_at",
        "updated_at",
    ]

    def get_permissions(self):
        permission_options = {
            "GET": [permissions.AllowAny()],
            "POST": [permissions.IsAuthenticated()],
        }
        permission = permission_options.get(self.request.method)

        if not permission:
            return [permissions.IsAuthenticated()]
        return permission

    @extend_schema(
        summary="게시글 목록 조회 및 검색API",
        tags=["게시글"],
        parameters=[
            OpenApiParameter(name="q", description="게시글 검색 키워드", required=False, type=OpenApiTypes.STR),
        ],
        responses=schema.article_render_response(many=True),
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary="게시글 생성 API",
        tags=["게시글"],
        request=ArticleCreateRenderRequest,
        responses=schema.article_render_response(),
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)
        return self.success_response(serializer.data, status_code=status.HTTP_201_CREATED)


class ArticleDetailAPI(BaseAPIView):
    service = ArticleService()

    def get_permissions(self):
        permission_options = {
            "GET": [permissions.AllowAny()],
            "PUT": [permissions.IsAuthenticated(), IsOwnerOrReadOnly()],
            "DELETE": [permissions.IsAuthenticated(), IsOwnerOrReadOnly()],
        }
        permission = permission_options.get(self.request.method)

        if not permission:
            return [permissions.IsAuthenticated()]
        return permission

    @property
    def author_id(self):
        return self.request.user.uuid

    @extend_schema(
        summary="상세 게시글 조회 API",
        tags=["게시글"],
        request=UuidSerializer,
        responses=schema.ArticleOutputSchema(),
    )
    def get(self, request, article_id):
        article = self.service.get_article(article_id)
        if not article:
            return self.fail_response(message="Does not found article", status_code=404)

        output_serializer = ArticleSerializer(article)
        viewer_ip = request.META.get("REMOTE_ADDR")
        ArticleView.record_view(article=article, viewer_ip=viewer_ip)
        return self.success_response(output_serializer.data, message="success retrieved!")

    @extend_schema(
        summary="게시글 수정 API",
        tags=["게시글"],
        request=UuidSerializer,
        responses=schema.ArticleOutputSchema(),
    )
    def put(self, request, article_id):
        updated_product = self.service.update_article(article_id, self.author_id, request.data)
        output_serializer = ArticleSerializer(updated_product)
        return self.success_response(output_serializer.data, message="success updated!")

    @extend_schema(
        summary="게시글 삭제 API",
        tags=["게시글"],
        request=UuidSerializer,
        responses={200: DeleteOutputSchema()},
    )
    def delete(self, request, article_id):
        self.service.delete_article(article_id, self.author_id)
        return self.success_response(message="[HARD DELETE] deleted successfully!")
