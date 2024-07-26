from drf_spectacular.utils import extend_schema

from core_apps.profiles.services.profile_query import ProfileQuery
from core_apps.shared.apis import BaseAPIView
from core_apps.shared.swaggers import (
    CommonRenderResponse,
    UuidSerializer,
    result_serializer,
)


class FollowAPIView(BaseAPIView):
    class FollowRenderSerializer(CommonRenderResponse):
        results = result_serializer(component_name="follow")

    @extend_schema(
        summary="팔로우 등록 API",
        tags=["팔로우"],
        request=UuidSerializer,
        responses=FollowRenderSerializer,
    )
    def post(self, request, user_id):
        follower = ProfileQuery.get_profile_by_user(user=request.user)
        user_profile = request.user.profile
        profile = ProfileQuery.get_profile_by_user_uuid(uuid=user_id)

        if profile == follower:  # NOTE: 자기 자신을 팔로우 하는 경우
            return self.fail_response(message="you can't follow yourself")

        if user_profile.is_following(profile):
            return self.fail_response(message=f"you are already following {profile.user.username}")

        user_profile.follow(profile)
        return self.success_response(message=f"You are now following {profile.user.username}")


class UnfollowAPIView(BaseAPIView):
    class FollowRenderSerializer(CommonRenderResponse):
        results = result_serializer(component_name="follow")

    @extend_schema(
        summary="팔로우 취소 API",
        tags=["팔로우"],
        request=UuidSerializer,
        responses=FollowRenderSerializer,
    )
    def post(self, request, user_id):
        user_profile = request.user.profile
        profile = ProfileQuery.get_profile_by_user_uuid(uuid=user_id)
        username = profile.user.username

        if not user_profile.is_following(profile):
            return self.fail_response(
                message=f"you can't unfollow {username}, since you were not following then in the first place"
            )

        user_profile.unfollow(profile)
        return self.success_response(message=f"You are now unfollowed {profile.user.username}")
