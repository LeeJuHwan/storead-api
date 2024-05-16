from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status


class BookListAPIViewSchema:
    def __call__(self, cls):
        cls = extend_schema_view(
            get=extend_schema(
                summary="책 목록 조회 API",
                tags=["책"],
            ),
            post=extend_schema(
                summary="책 생성 API",
                tags=["책"],
            ),
        )(cls)
        return cls


class BookDetailDocument:
    default_summary = "책 상세 정보 조회 API"
    default_tags = ["책"]

    def __init__(self, summary=None, tags=None, request_serializer=None, response_serializer=None):
        self.request_serializer = request_serializer
        self.response_serializer = response_serializer
        self.summary = summary if summary else self.default_summary
        self.tags = [tags] if tags else self.default_tags

    def __call__(self, func):
        @extend_schema(
            summary=self.summary,
            tags=["책"],
            request=self.request_serializer,
            responses={status.HTTP_200_OK: self.response_serializer},
        )
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
