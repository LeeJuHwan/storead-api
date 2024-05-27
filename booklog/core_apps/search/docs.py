from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter

search_parameter = OpenApiParameter(
    name="search",
    description="검색어를 입력합니다.",
    required=True,
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    examples=[
        OpenApiExample(
            "제목 검색",
            value="제목",
            description="제목에 '제목'이 포함된 게시글을 검색합니다.",
        ),
        OpenApiExample(
            "내용 검색",
            value="내용",
            description="내용에 '내용'이 포함된 게시글을 검색합니다.",
        ),
    ],
)

ordering_parameter = OpenApiParameter(
    name="ordering",
    description="결과 정렬 순서를 지정합니다.",
    required=False,
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    examples=[
        OpenApiExample(
            "최신순",
            value="-created_at",
            description="생성 날짜 기준으로 내림차순 정렬",
        ),
        OpenApiExample(
            "과거순",
            value="created_at",
            description="생성 날짜 기준으로 오름차순 정렬",
        ),
        OpenApiExample(
            "조회수순",
            value="-view_count",
            description="조회수 기준으로 내림차순 정렬",
        ),
    ],
)
