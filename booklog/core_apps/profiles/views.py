import logging

from core_apps.common.swaggers import (
    CommonRenderResponse,
    UuidSerializer,
    result_serializer,
)
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..common.apis import BaseAPIView
from .models import Profile
from .queries import ProfileQuery
from .serializers import (
    FollowingSerializer,
    FollowResponseSerializer,
    ProfileSerializer,
    UpdateProfileSerializer,
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
