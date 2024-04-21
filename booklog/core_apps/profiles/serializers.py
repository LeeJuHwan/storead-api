from rest_framework import serializers

from .models import Profile
from .exceptions import EmptyUserNameException


class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.username")
    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "id",
            "name",
            "profile_photo",
            "about_me",
        ]

    def get_profile_photo(self, obj):
        return obj.profile_photo.url if obj.profile_photo else None


class UpdateProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.username")

    class Meta:
        model = Profile
        fields = [
            "name",
            "profile_photo",
            "about_me",
        ]

    # NOTE: 유저랑 관계형을 맺고 있기 때문에 upadte를 직접적으로 명시 해야함
    def update(self, instance, validated_data):
        self.fields.pop("name")
        user_data = validated_data.pop('user', {})
        username = user_data.get('username')

        if username:
            instance.user.username = username
            instance.user.save()
        # NOTE: 유저가 자신의 이름을 설정하지 않은 경우
        else:
            raise EmptyUserNameException()

        for field in self.fields:
            input_data = validated_data.get(field, getattr(instance, field))
            setattr(instance, field, input_data)
        instance.save()

        return instance
