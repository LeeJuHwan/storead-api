from typing import Optional

from core_apps.articles.exceptions import ArticleIdNotFound
from core_apps.articles.services.article_query import ArticleQuery
from core_apps.comments.exceptions import CommentNotFound, CommentPermissionDenied
from core_apps.comments.models import Comment
from core_apps.comments.serializers.comment_serializer import CommentSerializer
from core_apps.comments.services.comment_query import CommentQuery


class CommentService:
    model = Comment
    query = CommentQuery()
    article_query = ArticleQuery()

    @staticmethod
    def has_own_permission(comment_writer, request_user) -> bool:
        if comment_writer != request_user:
            return False

        return True

    def get_comment(self, comment_id: str) -> Optional[Comment]:
        return self.query.get_comment_by_id(comment_id)

    def create_comment(self, article_id, validated_data, writer):
        parent_comment_uuid: Optional[Comment] = validated_data.get("parent_comment")

        if parent_comment := self.query.get_comment_by_id_with_article_id(article_id, parent_comment_uuid):
            print(f"parent comment: {parent_comment}")
            validated_data["parent_comment"] = parent_comment

        article = self.article_query.get_article_by_uuid(article_id)

        if not article:
            raise ArticleIdNotFound
        return Comment.objects.create(article=article, user=writer, **validated_data)

    def update_comment(self, comment_id, user, data):
        comment: Optional[Comment] = self.get_comment(comment_id)

        if not self.has_own_permission(comment.user, user):
            raise CommentPermissionDenied()
        if not comment:
            raise CommentNotFound()

        input_serializer = CommentSerializer(comment, data=data, partial=True)
        input_serializer.is_valid(raise_exception=True)
        return input_serializer.save()

    def delete_comment(self, comment_id, user):
        comment: Optional[Comment] = self.get_comment(comment_id)

        if not self.has_own_permission(comment.user, user):
            raise CommentPermissionDenied()

        comment.delete()
