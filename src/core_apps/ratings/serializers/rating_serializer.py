from rest_framework import serializers

from core_apps.ratings.models import Rating


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ["rating"]
