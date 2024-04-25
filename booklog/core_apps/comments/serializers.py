from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    article_title = serializers.CharField(source="article.title", read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "username",
            "article_title",
            "parent_comment",
            "content",
            "created_at",
        ]
