from core_apps.comments.models import Comment


class CommentQuery:
    def get_comment_by_id_with_article_id(self, article_id, comment_uuid):
        try:
            return Comment.objects.select_related("article").get(article__id=article_id, id=comment_uuid)
        except Comment.DoesNotExist:
            return

    def get_comment_by_id(self, comment_uuid):
        try:
            return Comment.objects.get(id=comment_uuid)
        except Comment.DoesNotExist:
            return
