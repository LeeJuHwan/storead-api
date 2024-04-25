from typing import Dict
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from .models import SocialUser
from .services import SocialOAuthService
from .exceptions import IncorrectSocialType
from .tokens import token_refresh


class SocialLoginServiceMixin(APIView, SocialOAuthService):
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
                raise IncorrectSocialType()

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


class KakaoLogin(SocialLoginServiceMixin):
    platform = "kakao"
    uuid_key = "id"

    def get_username(self, user_profile: Dict[str, str | Dict]) -> str:
        kakao_account = user_profile.get("properties")
        uuid = self.get_user_uuid(user_profile)[:4]

        if not kakao_account:
            return f"Unkown{uuid}"

        return kakao_account.get("nickname", f"Unkown{uuid}")


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


class SocialLogutAPI(APIView, SocialOAuthService):
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        return self.social_logout()


class TokenRefreshAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request: Request) -> Response:
        return token_refresh(request)
