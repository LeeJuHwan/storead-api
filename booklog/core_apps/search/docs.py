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


suggest_parameter = OpenApiParameter(
    name="title__completion",
    description="자동 완성 검색 내용",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    examples=[
        OpenApiExample(name="검색 제목", value="검색 할 내용", description="suggest?title__completion={value} 형태")
    ],
)


auto_suggest_response = OpenApiExample(
    name="자동 완성 결과",
    response_only=True,
    value={
        "title__completion": [
            {
                "text": "검색한 텍스트",
                "offset": 0,
                "length": "텍스트 길이",
                "options": [
                    {
                        "text": "게시글 제목",
                        "_index": "ElasticSearch Engine Index 이름",
                        "_type": "인덱스 타입",
                        "_id": "인덱스 번호",
                        "_score": "자동 완성 적합 스코어",
                        "_source": {
                            "title": "책 제목",
                            "description": "책 내용 미리보기",
                            "body": "책 내용",
                            "author_username": "게시글 작성자",
                            "tags": [
                                "게시글 태그 목록1",
                                "게시글 태그 목록2",
                            ],
                            "book_title": "책 제목",
                            "created_at": "게시글 작성 일자",
                        },
                    }
                ],
            }
        ]
    },
    status_codes=[200],
)
