from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.username")
    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "pkid",
            "name",
            "profile_photo",
            "about_me",
        ]

    def get_profile_photo(self, obj):
        return obj.profile_photo.url if obj.profile_photo else None


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "name",
            "profile_photo",
            "about_me",
        ]
