from core_apps.common.swaggers import UuidSerializer
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import (
    AlreadyFollowing,
    CantFollowYourSelf,
    CantUnfollowNotFollowingUser,
)
from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import FollowingSerializer, ProfileSerializer, UpdateProfileSerializer


class MyProfileDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    renderer_classes = [ProfileJSONRenderer]

    def get_queryset(self):
        queryset = Profile.objects.select_related("user")
        return queryset

    def get_object(self):
        user = self.request.user
        profile = self.get_queryset().get(user=user)
        return profile

    @extend_schema(
        summary="나의 프로필 상세 정보 조회 API",
        tags=["프로필"],
        responses=ProfileSerializer,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserProfileDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    renderer_classes = [ProfileJSONRenderer]

    @extend_schema(
        summary="다른 유저 프로필 상세 정보 조회 API",
        tags=["프로필"],
        request=UuidSerializer,
        responses=ProfileSerializer,
    )
    def get(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileAPIView(generics.UpdateAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]

    class ProfileRenderResponse(serializers.Serializer):
        status_code = serializers.IntegerField()
        profile = ProfileSerializer()

    def get_object(self) -> Profile:
        profile = self.request.user.profile
        return profile

    @extend_schema(
        summary="프로필 수정 API",
        tags=["프로필"],
        request=UpdateProfileSerializer,
        responses={status.HTTP_200_OK: ProfileRenderResponse},
    )
    def patch(self, request) -> Response:
        instance: Profile = self.get_object()
        serializer: UpdateProfileSerializer = self.get_serializer(instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            return Response(e, status=e.status_code or status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowAPIView(APIView):
    class FollowSerializer(serializers.Serializer):
        status_code = serializers.IntegerField()
        message = serializers.CharField()

    @extend_schema(
        summary="팔로우 등록 API",
        tags=["팔로우"],
        request=UuidSerializer,
        responses={status.HTTP_200_OK: FollowSerializer},
    )
    def post(self, request, user_id):
        try:
            follower = Profile.objects.get(user=self.request.user)
            user_profile = request.user.profile
            profile = Profile.objects.get(user__uuid=user_id)

            if profile == follower:  # NOTE: 자기 자신을 팔로우 하는 경우
                raise CantFollowYourSelf()

            if user_profile.is_following(profile):
                raise AlreadyFollowing(profile.user.username)

            user_profile.follow(profile)
            return Response(
                {
                    "status_code": status.HTTP_200_OK,
                    "message": f"You are now following {profile.user.username}",
                }
            )
        except Profile.DoesNotExist:
            raise NotFound("You can't follow a profile that does not exist.")


class UnfollowAPIView(APIView):
    class FollowSerializer(serializers.Serializer):
        status_code = serializers.IntegerField()
        message = serializers.CharField()

    @extend_schema(
        summary="팔로우 취소 API",
        tags=["팔로우"],
        request=UuidSerializer,
        responses=FollowSerializer,
    )
    def post(self, request, user_id):
        user_profile = request.user.profile
        profile = Profile.objects.get(user__uuid=user_id)

        if not user_profile.is_following(profile):
            raise CantUnfollowNotFollowingUser(profile.user.username)

        user_profile.unfollow(profile)
        context = {
            "status_code": status.HTTP_200_OK,
            "message": f"You have unfollowed {profile.user.username}",
        }
        return Response(context, status.HTTP_200_OK)


class FollowingListView(APIView):
    permission_classes = [IsAuthenticated]

    class FollowListSerializer(serializers.Serializer):
        status_code = serializers.IntegerField()
        followers_count = serializers.IntegerField()
        following = FollowingSerializer(many=True)

    @extend_schema(
        summary="팔로잉 목록 조회 API",
        tags=["팔로우"],
        request=None,
        responses=FollowListSerializer,
    )
    def get(self, request):
        profile = get_object_or_404(Profile, user__uuid=request.user.uuid)
        following_profiles = profile.followers.all()
        following_serializer = FollowingSerializer(following_profiles, many=True)
        response_data = {
            "status_code": status.HTTP_200_OK,
            "followers_count": following_profiles.count(),
            "following": following_serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class FollowerListView(APIView):
    permission_classes = [IsAuthenticated]

    class FollowListSerializer(serializers.Serializer):
        status_code = serializers.IntegerField()
        followers_count = serializers.IntegerField()
        followers = FollowingSerializer(many=True)

    @extend_schema(
        summary="팔로워 목록 조회 API",
        tags=["팔로우"],
        responses=FollowListSerializer,
    )
    def get(self, request):
        profile = get_object_or_404(Profile, user__uuid=request.user.uuid)
        follower_profiles = profile.following.all()
        serializer = FollowingSerializer(follower_profiles, many=True)
        response = {
            "status_code": status.HTTP_200_OK,
            "followers_count": follower_profiles.count(),
            "followers": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)
