from drf_spectacular.utils import extend_schema, extend_schema_view


class ProfileDetailAPIViewSchema:
    def __call__(self, cls):
        cls = extend_schema_view(
            patch=extend_schema(
                summary="프로필 수정 API",
                tags=["프로필"],
            ),
            get=extend_schema(
                summary="나의 프로필 상세 정보 조회 API",
                tags=["프로필"],
            ),
        )(cls)
        return cls


class FollowingDetailAPIViewSchema:
    def __call__(self, cls):
        cls = extend_schema_view(
            post=extend_schema(
                summary="팔로우 등록 API",
                tags=["팔로우"],
            ),
            get=extend_schema(
                summary="나의 프로필 상세 정보 조회 API",
                tags=["프로필"],
            ),
        )(cls)
        return cls
