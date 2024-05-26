from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    article_title = serializers.CharField(source="article.title", read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "pkid",
            "id",
            "username",
            "article_title",
            "parent_comment",
            "content",
            "created_at",
            "replies",
        ]

    def get_replies(self, instance):
        serializer = self.__class__(instance.replies, many=True)
        serializer.bind("", self)
        return serializer.data
