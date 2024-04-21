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


class KakaoLogin(SocialLoginServiceMixin):
    platform = "kakao"
    uuid_key = "id"


class GithubLogin(SocialLoginServiceMixin):
    platform = "github"
    uuid_key = "id"


class SocialLogutAPI(APIView, SocialOAuthService):
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        return self.social_logout()


class TokenRefreshAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request: Request) -> Response:
        return token_refresh(request)
