from typing import Dict

from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenVerifyView

from core_apps.shared.apis import BaseAPIView
from core_apps.shared.swaggers import OutputSerializer
from core_apps.social_users.models import SocialUser
from core_apps.social_users.services import SocialOAuthService
from core_apps.social_users.services.tokens import token_refresh


class SocialLoginServiceMixin(BaseAPIView, SocialOAuthService):
    permission_classes = (AllowAny,)
    platform: str = None

    def get(self, request: Request) -> Response:
        code: str = request.GET.get("code")
        access_token: str = self.get_access_token(code)

        user_profile_request: Request = self.get_user_profile(access_token)

        try:
            uuid: str = self.get_user_uuid(user_profile_request)
            user: SocialUser = SocialUser.objects.get(uuid=uuid)

            if user.provider != self.platform:
                return self.fail_response(message="incorrect social type.")

            return self.social_login(user)

        except SocialUser.DoesNotExist:
            return self.register(user_profile_request)

        except Exception as e:
            response_message = {"error": str(e)}
            return Response(response_message, status=e.status_code or status.HTTP_400_BAD_REQUEST)


class GoogleLogin(SocialLoginServiceMixin):
    platform = "google"
    uuid_key = "user_id"

    def get_username(self, user_profile: Dict[str, str | Dict]) -> str:
        user_email = user_profile.get("email")

        if not user_email:
            uuid = self.get_user_uuid(user_profile)[:4]
            return f"Unkown{uuid}"

        return user_email.split("@")[0]

    @extend_schema(
        summary="구글 로그인 API",
        tags=["로그인"],
        parameters=[
            OpenApiParameter(name="code", description="구글 플랫폼 서버 인가 코드", required=True, type=str),
        ],
        responses=OutputSerializer,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class KakaoLogin(SocialLoginServiceMixin):
    platform = "kakao"
    uuid_key = "id"

    def get_username(self, user_profile: Dict[str, str | Dict]) -> str:
        kakao_account = user_profile.get("properties")
        uuid = self.get_user_uuid(user_profile)[:4]

        if not kakao_account:
            return f"Unkown{uuid}"

        return kakao_account.get("nickname", f"Unkown{uuid}")

    @extend_schema(
        summary="카카오 로그인 API",
        tags=["로그인"],
        parameters=[
            OpenApiParameter(name="code", description="카카오 플랫폼 서버 인가 코드", required=True, type=str),
        ],
        responses=OutputSerializer,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class GithubLogin(SocialLoginServiceMixin):
    platform = "github"
    uuid_key = "id"

    def get_username(self, user_profile: Dict[str, str | Dict]) -> str:
        """
        Get user username by the user profile.
        """
        username = user_profile.get("login")

        if not username:
            uuid = self.get_user_uuid(user_profile)[:4]
            return f"Unkown{uuid}"
        return username

    @extend_schema(
        summary="깃허브 로그인 API",
        tags=["로그인"],
        parameters=[
            OpenApiParameter(name="code", description="깃허브 플랫폼 서버 인가 코드", required=True, type=str),
        ],
        responses=OutputSerializer,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SocialLogutAPI(BaseAPIView, SocialOAuthService):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="소셜 로그아웃 API",
        tags=["로그아웃"],
        responses=OutputSerializer,
    )
    def post(self, request: Request) -> Response:
        return self.social_logout()


class TokenVerifyAPIView(TokenVerifyView):
    @extend_schema(
        summary="토큰 검증 API",
        tags=["토큰"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class TokenRefreshAPIView(BaseAPIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        summary="토큰 재발급 API",
        tags=["토큰"],
        responses=OutputSerializer,
    )
    def get(self, request: Request) -> Response:
        return token_refresh(request)
