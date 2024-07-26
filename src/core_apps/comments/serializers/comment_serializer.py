from rest_framework import serializers

from core_apps.comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    user_id = serializers.CharField(source="user.uuid", read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "pkid",
            "id",
            "username",
            "user_id",
            "parent_comment",
            "content",
            "created_at",
            "replies",
        ]

    def get_replies(self, instance):
        serializer = self.__class__(instance.replies, many=True)
        serializer.bind("", self)
        return serializer.data
