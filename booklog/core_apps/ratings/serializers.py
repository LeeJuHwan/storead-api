from rest_framework import serializers

from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    # article_title = serializers.CharField(source="article.title", read_only=True)

    class Meta:
        model = Rating
        fields = ["rating"]
