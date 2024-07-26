from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status

from core_apps.comments.models import Comment
from core_apps.comments.serializers import (
    CommentInputSerializer,
    CommentSerializer,
    render_response,
)
from core_apps.comments.services.comment_service import CommentService
from core_apps.shared.apis import BaseAPIView, BaseListAPIView
from core_apps.shared.swaggers import UuidSerializer


class CommentListCreateView(BaseListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    service = CommentService()

    @property
    def article_id(self):
        return self.kwargs.get("article_id")

    def get_queryset(self):
        return Comment.objects.filter(article__id=self.article_id, parent_comment=None)

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
        summary="댓글 목록 조회 API",
        tags=["댓글"],
        responses=render_response(),
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary="댓글 생성 API",
        tags=["댓글"],
        request=CommentInputSerializer,
        responses=render_response(),
    )
    def post(self, request, *args, **kwargs):
        input_serializer = CommentInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        comment = self.service.create_comment(
            article_id=self.article_id, validated_data=input_serializer.validated_data, writer=request.user
        )
        output_serializer = CommentSerializer(comment)
        return self.success_response(
            data=output_serializer.data, message="successfully created!", status_code=status.HTTP_201_CREATED
        )


class CommentUpdateDeleteView(BaseAPIView):
    service = CommentService()

    @extend_schema(
        summary="댓글 내용 수정 API",
        tags=["댓글"],
        request=CommentInputSerializer,
        responses=render_response(),
    )
    def put(self, request, comment_id):
        comment = self.service.update_comment(comment_id, request.user, request.data)
        output_serializer = CommentSerializer(comment)
        return self.success_response(
            output_serializer.data, message="successfully updated!", status_code=status.HTTP_200_OK
        )

    @extend_schema(
        summary="댓글 내용 삭제 API",
        tags=["댓글"],
        request=UuidSerializer,
    )
    def delete(self, request, comment_id):
        self.service.delete_comment(comment_id, request.user)
        return self.success_response(message="[HARD DELETE] deleted successfully!", status_code=204)
