from rest_framework import serializers


class BookInputSerializer(serializers.Serializer):
    isbn = serializers.CharField()
    description = serializers.CharField()
    title = serializers.CharField()
    author = serializers.CharField()
    published_date = serializers.CharField()
    thumbnail_url = serializers.ImageField(required=False)


class BookOutputSerializer(serializers.Serializer):
    pkid = serializers.IntegerField()
    id = serializers.UUIDField()
    created_at = serializers.CharField()
    isbn = serializers.CharField()
    title = serializers.CharField()
    author = serializers.CharField()
    published_date = serializers.CharField()
    description = serializers.CharField()
    thumbnail_url = serializers.ImageField()
