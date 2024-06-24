from django.db import IntegrityError
from rest_framework import serializers

from .exceptions import AlreadyUseUserNameError
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.username")
    user_id = serializers.CharField(source="user.uuid")
    profile_id = serializers.CharField(source="id")
    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "profile_id",
            "user_id",
            "name",
            "profile_photo",
            "about_me",
        ]

    def get_profile_photo(self, obj):
        return obj.profile_photo.url if obj.profile_photo else None


class UpdateProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.username", required=False)

    class Meta:
        model = Profile
        fields = [
            "name",
            "profile_photo",
            "about_me",
        ]

    # NOTE: 유저랑 관계형을 맺고 있기 때문에 upadte를 직접적으로 명시 해야함
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        username = user_data.get("username")

        for field in self.fields:
            if field == "name":
                continue

            input_data = validated_data.get(field, getattr(instance, field))
            setattr(instance, field, input_data)

        # NOTE: 유저네임이 제공되었고, 기존 유저네임과 다른 경우에만 업데이트
        if username and username != instance.user.username:
            instance.user.username = username
            try:
                instance.user.save()
            except IntegrityError:
                raise AlreadyUseUserNameError()

        instance.save()
        return instance


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
