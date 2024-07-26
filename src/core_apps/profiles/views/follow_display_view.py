from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny

from core_apps.profiles.serializers import FollowingSerializer, FollowResponseSerializer
from core_apps.profiles.services.profile_query import ProfileQuery
from core_apps.shared.apis import BaseAPIView
from core_apps.shared.swaggers import CommonRenderResponse, result_serializer


class MyFollowerListView(BaseAPIView):
    permission_classes = [AllowAny]

    class FollowerRenderSerializer(CommonRenderResponse):
        results = result_serializer(obj=FollowResponseSerializer(), component_name="follower")

    @extend_schema(
        summary="팔로워 목록 조회 API",
        tags=["팔로우"],
        responses=FollowerRenderSerializer(),
    )
    def get(self, request):
        profile = ProfileQuery.get_profile_by_user_uuid(uuid=request.user.uuid)
        follower_profiles = profile.following.all()
        serializer = FollowingSerializer(follower_profiles, many=True)
        response_data = {
            "followers_count": follower_profiles.count(),
            "followers": serializer.data,
        }
        return self.success_response(response_data)


class UserFollowingListView(BaseAPIView):
    permission_classes = [AllowAny]

    class FollowerRenderSerializer(CommonRenderResponse):
        results = result_serializer(obj=FollowResponseSerializer(), component_name="following")

    @extend_schema(
        summary="팔로잉 목록 조회 API",
        tags=["팔로우"],
        request=None,
        responses=FollowerRenderSerializer,
    )
    def get(self, request, user_id):
        profile = ProfileQuery.get_profile_by_profile_id(profile_id=user_id)
        following_profiles = profile.followers.all()
        following_serializer = FollowingSerializer(following_profiles, many=True)
        response_data = {
            "followers_count": following_profiles.count(),
            "following": following_serializer.data,
        }
        return self.success_response(response_data)


class UserFollowerListView(BaseAPIView):
    permission_classes = [AllowAny]

    class FollowerRenderSerializer(CommonRenderResponse):
        results = result_serializer(obj=FollowResponseSerializer(), component_name="follower")

    @extend_schema(
        summary="팔로워 목록 조회 API",
        tags=["팔로우"],
        responses=FollowerRenderSerializer(),
    )
    def get(self, request, user_id):
        profile = ProfileQuery.get_profile_by_user_uuid(uuid=user_id)
        follower_profiles = profile.following.all()
        serializer = FollowingSerializer(follower_profiles, many=True)
        response_data = {
            "followers_count": follower_profiles.count(),
            "followers": serializer.data,
        }
        return self.success_response(response_data)
