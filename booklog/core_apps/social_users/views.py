from typing import Optional
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .domain import SocialPlatform


class BaseSocialLogin(APIView):
    permission_classes = (AllowAny,)

    client_id: str = None
    client_secret: str = None
    redirect_uri: str = None
    state: Optional[str] = None
    platform: str = None

    @property
    def social_domain(self):
        oauth_info = getattr(SocialPlatform, self.platform, None)

        if not oauth_info:
            raise ValueError(f"{self.platform} is not supported")

        return oauth_info.info.to_dict()

    @property
    def auth(self):
        return {
            "platform": self.platform,
            "fields": {attr: value for attr, value in self.social_domain.items() if value}}

    def get(self, request):
        request_dict = dict(request.META)
        print(f"auth: {self.auth}")

        # TODO: 응답 값 수정
        context = {
            "request": request_dict.get("REQUEST_METHOD"),
            "endpoint": request_dict.get("PATH_INFO"),
            "client_ip": request_dict.get("REMOTE_ADDR"),
            }

        return Response(context, status=status.HTTP_200_OK)


class GoogleLogin(BaseSocialLogin):
    platform = "google"


class KakaoLogin(BaseSocialLogin):
    platform = "kakao"


class GithubLogin(BaseSocialLogin):
    platform = "github"
