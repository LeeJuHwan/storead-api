from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class BaseSocialLogin(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        request_dict = dict(request.META)
        payload = {
            "request": request_dict.get("REQUEST_METHOD"),
            "endpoint": request_dict.get("PATH_INFO"),
            "client_ip": request_dict.get("REMOTE_ADDR"),
            }
        return Response(payload, status=status.HTTP_200_OK)


class GoogleLogin(BaseSocialLogin):
    pass


class KakaoLogin(BaseSocialLogin):
    pass


class GithubLogin(BaseSocialLogin):
    pass
