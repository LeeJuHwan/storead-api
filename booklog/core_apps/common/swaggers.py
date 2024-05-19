from rest_framework import serializers


class UuidSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()


class OutputSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    message = serializers.CharField()
