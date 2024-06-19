from typing import Optional

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .exceptions import EmptyTokenException


def token_refresh(request) -> Response:
    """
    request access tokens with refresh tokens
    """
    refresh_token: Optional[str] = request.COOKIES.get("refresh_token", None)

    if not refresh_token:
        raise EmptyTokenException()

    data = {"message": "successfully refreshed token"}
    response: Response = Response(data, status=status.HTTP_200_OK)

    try:
        refresh = RefreshToken(refresh_token)
        access_token_lifetime = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
        response.set_cookie("access_token", str(refresh.access_token), max_age=access_token_lifetime)

    except EmptyTokenException as e:
        return Response({"detail": str(e)}, status=e.status_code)

    return response
