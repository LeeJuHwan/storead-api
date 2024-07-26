from rest_framework import serializers

from core_apps.profiles.models import Profile


class FollowingSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "name",
            "profile_photo",
            "about_me",
        ]


class FollowResponseSerializer(serializers.Serializer):
    followers_count = serializers.IntegerField()
    following = FollowingSerializer(many=True)
