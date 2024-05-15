from drf_spectacular.utils import extend_schema
from rest_framework import status


class BookDetailDocument:
    def __init__(self, request_serializer=None, response_serializer=None):
        self.request_serializer = request_serializer
        self.response_serializer = response_serializer

    def __call__(self, func):
        @extend_schema(
            summary="책 상세 정보 조회 API",
            tags=["책"],
            request=self.request_serializer,
            responses={status.HTTP_200_OK: self.response_serializer},
        )
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
