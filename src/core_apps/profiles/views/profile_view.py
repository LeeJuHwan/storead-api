import logging

from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core_apps.profiles.models import Profile
from core_apps.profiles.serializers import (
    FollowingSerializer,
    FollowResponseSerializer,
    ProfileSerializer,
    UpdateProfileSerializer,
)
from core_apps.profiles.services.profile_query import ProfileQuery
from core_apps.shared.apis import BaseAPIView
from core_apps.shared.swaggers import (
    CommonRenderResponse,
    UuidSerializer,
    result_serializer,
)

logger = logging.getLogger("django")


class MyProfileDetailAPIView(BaseAPIView):
    class ProfileRenderResponse(CommonRenderResponse):
        results = result_serializer(ProfileSerializer())

    @extend_schema(summary="나의 프로필 상세 정보 조회 API", tags=["프로필"], responses=ProfileRenderResponse())
    def get(self, request, *args, **kwargs):
        user = self.request.user

        profile = ProfileQuery.get_profile_by_user(user=user)
        serializer = ProfileSerializer(profile)
        return self.success_response(data=serializer.data, message="Profile successfully retrieved")


class UserProfileDetailAPIView(BaseAPIView):
    permission_classes = [AllowAny]

    class ProfileRenderResponse(CommonRenderResponse):
        results = result_serializer(ProfileSerializer())

    @extend_schema(
        summary="다른 유저 프로필 상세 정보 조회 API",
        tags=["프로필"],
        request=UuidSerializer,
        responses=ProfileRenderResponse,
    )
    def get(self, request, profile_id):
        profile = ProfileQuery.get_profile_by_profile_id(profile_id)
        serializer = ProfileSerializer(profile)
        return self.success_response(
            data=serializer.data, message=f"{profile.user.username}'s profile successfully retrieved"
        )


class UpdateProfileAPIView(BaseAPIView):
    class ProfileRenderResponse(CommonRenderResponse):
        results = result_serializer(ProfileSerializer())

    @extend_schema(
        summary="프로필 수정 API",
        tags=["프로필"],
        request=UpdateProfileSerializer,
        responses=ProfileRenderResponse,
    )
    def put(self, request) -> Response:
        instance: Profile = self.request.user.profile
        serializer: UpdateProfileSerializer = UpdateProfileSerializer(instance, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except APIException as e:
            return self.fail_response(data=request.data, message=e.detail)

        return self.success_response(data=serializer.data, message="Successfully update profile")


class MyFollowingListView(BaseAPIView):
    permission_classes = [AllowAny]

    class FollowerRenderSerializer(CommonRenderResponse):
        results = result_serializer(obj=FollowResponseSerializer(), component_name="following")

    @extend_schema(
        summary="팔로잉 목록 조회 API",
        tags=["팔로우"],
        request=None,
        responses=FollowerRenderSerializer,
    )
    def get(self, request):
        profile = ProfileQuery.get_profile_by_user_uuid(uuid=request.user.uuid)
        following_profiles = profile.followers.all()
        following_serializer = FollowingSerializer(following_profiles, many=True)
        response_data = {
            "followers_count": following_profiles.count(),
            "following": following_serializer.data,
        }
        return self.success_response(response_data)
