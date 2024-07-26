from rest_framework import serializers

from core_apps.comments.serializers.comment_serializer import CommentSerializer
from core_apps.shared.swaggers import result_serializer


class CommentInputSerializer(serializers.Serializer):
    content = serializers.CharField()
    parent_comment = serializers.CharField(allow_null=True, required=False)


def render_response(many=False):
    return result_serializer(obj=CommentSerializer(many=many), component_name="comments")
