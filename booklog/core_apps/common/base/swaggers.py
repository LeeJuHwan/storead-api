from drf_spectacular.utils import extend_schema
from rest_framework import status


class BaseSwagger:
    default_summary = None
    default_tags = None

    def __init__(self, summary=None, tags=None, request_serializer=None, response_serializer=None):
        self.request_serializer = request_serializer
        self.response_serializer = response_serializer
        self.summary = summary if summary else self.default_summary
        self.tags = [tags] if tags else self.default_tags

    def __call__(self, func):
        @extend_schema(
            summary=self.summary,
            tags=self.tags,
            request=self.request_serializer,
            responses={status.HTTP_200_OK: self.response_serializer},
        )
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
