from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    article_title = serializers.CharField(source="article.title", read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "username",
            "article_title",
            "parent_comment",
            "content",
            "created_at",
            "replies",
        ]

    def create(self, validated_data):
        print(f"validated_data: {validated_data}")
        parent_comment_id = validated_data.get("parent_comment")
        if parent_comment_id:
            parent_comment = Comment.objects.get(id=parent_comment_id)
            validated_data["parent_comment"] = parent_comment
        return super().create(validated_data)

    def get_replies(self, instance):
        serializer = self.__class__(instance.replies, many=True)
        serializer.bind("", self)
        return serializer.data
