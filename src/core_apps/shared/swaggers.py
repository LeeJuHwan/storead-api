from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers


class UuidSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()


class OutputSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    message = serializers.CharField()


class CommonRenderResponse(serializers.Serializer):
    status_code = serializers.IntegerField()
    status = serializers.BooleanField()


class NoContentSerializer(serializers.Serializer):
    data = serializers.CharField()
    message = serializers.CharField()


class DeleteOutputSchema(CommonRenderResponse):
    results = NoContentSerializer()


def result_serializer(obj=None, component_name=None):
    if not component_name:
        import uuid

        component_name = f"DefaultSerializer_{uuid.uuid4()}"

    # NOTE: Swagger UI 생성 시 동일한 시리얼라이저를 재사용 하면 필드 값 마저 재사용 되기 때문에 고유의 값으로 변경
    @extend_schema_serializer(component_name=component_name)
    class DefaultSerializer(serializers.Serializer):
        data = obj
        message = serializers.CharField()

    return DefaultSerializer()
