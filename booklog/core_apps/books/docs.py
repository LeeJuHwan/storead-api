from core_apps.common.base.swaggers import BaseSwagger
from drf_spectacular.utils import extend_schema, extend_schema_view


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


class BookDetailDocument(BaseSwagger):
    default_summary = "책 상세 정보 조회 API"
    default_tags = ["책"]

    def __init__(self, summary=None, tags=None, request_serializer=None, response_serializer=None):
        super().__init__(summary, tags, request_serializer, response_serializer)
