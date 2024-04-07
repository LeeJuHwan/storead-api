from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny

from .models import SocialUser
from .services import SocialOAuthService


class SocialServiceMixin(APIView, SocialOAuthService):
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
                response_message = {"error": "no matching social type"}
                return Response(response_message, status=status.HTTP_400_BAD_REQUEST)

            return self.login(user)

        except SocialUser.DoesNotExist:
            self.register(user_profile_request)


class GoogleLogin(SocialServiceMixin):
    platform = "google"
    uuid_key = "user_id"


class KakaoLogin(SocialServiceMixin):
    platform = "kakao"
    uuid_key = "id"


class GithubLogin(SocialServiceMixin):
    platform = "github"
    uuid_key = "id"
