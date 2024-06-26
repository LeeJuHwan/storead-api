from core_apps.common.swaggers import UuidSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404

from .models import Article, Comment
from .serializers import CommentSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        article_id = self.kwargs.get("article_id")
        return Comment.objects.filter(article__id=article_id, parent_comment=None)

    def perform_create(self, serializer):
        user = self.request.user
        article_id = self.kwargs.get("article_id")
        article = get_object_or_404(Article, id=article_id)
        serializer.save(user=user, article=article)

    @extend_schema(
        summary="댓글 목록 조회 API",
        tags=["댓글"],
        responses=CommentSerializer,
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary="댓글 생성 API",
        tags=["댓글"],
        request=CommentSerializer,
        responses=CommentSerializer,
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CommentUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "id"

    def perform_update(self, serializer):
        user = self.request.user
        comment = self.get_object()

        if user != comment.user:
            raise PermissionDenied("You do not have permission to edit this comment.")
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        comment = self.get_object()

        if user != comment.user:
            raise PermissionDenied("You do not have permission to delete this comment.")
        instance.delete()

    @extend_schema(
        summary="댓글 상세 조회 API",
        tags=["댓글"],
        request=UuidSerializer,
        responses=CommentSerializer,
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="댓글 내용 수정 API",
        tags=["댓글"],
        request=CommentSerializer,
        responses=CommentSerializer,
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="댓글 내용 삭제 API",
        tags=["댓글"],
        request=UuidSerializer,
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
