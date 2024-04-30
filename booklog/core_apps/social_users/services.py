from datetime import timedelta
from typing import Dict, Optional, Union

import requests
from django.conf import settings
from django.contrib.auth.models import update_last_login
from requests.models import Response as RequestsResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .domain import (
    GithubAuth,
    GoogleAuth,
    KakaoAuth,
    PlatformRequestUrl,
    SocialPlatform,
)
from .exceptions import (
    DoesNotSupportPlatform,
    EmptyTokenException,
    InvalidAuthorizationCode,
    PlatformServerException,
)
from .models import SocialUser

SOCIAL_TYPES = Union[GoogleAuth, KakaoAuth, GithubAuth]


class SocialOAuthService:
    client_id: str = None
    client_secret: str = None
    redirect_uri: str = None
    state: Optional[str] = None
    platform: str = None
    uuid_key: str = None
    _auth: Optional[Dict[str, Dict[str, str | int]]] = None

    @property
    def social_domain(self) -> Dict[str, str]:
        """
        Return the domain of the social platform.
        """
        oauth: Optional[SOCIAL_TYPES] = getattr(SocialPlatform, self.platform, None)

        if not oauth:
            raise ValueError(f"{self.platform} is not supported")

        return oauth.info.to_dict()

    @property
    def auth(self) -> Dict[str, Dict[str, str]]:
        """
        Return the authorization information.
        """
        if self._auth is None:
            self._auth: Dict[str, str] = {attr: value for attr, value in self.social_domain.items() if value}
        return self._auth

    @property
    def oauth_request_url(self) -> str:
        """
        Return domain of the oauth request url.
        """
        return self.auth.get("token_info_api")

    def _add_authorize_code(self, code: str):
        """
        Add authorization code.
        """
        self.auth.update({"code": code})

    def _request_access_token(self) -> RequestsResponse:
        """
        Authorize the client with the authorization code.
        """
        platform_request_url: Optional[str] = getattr(PlatformRequestUrl, self.platform, None)

        if not platform_request_url:
            raise DoesNotSupportPlatform()

        token_request_call_endpoint: str = platform_request_url.format(**self.auth)
        return requests.post(token_request_call_endpoint, headers={"Accept": "application/json"})

    def get_access_token(self, code: Optional[str]) -> str:
        """
        Access token by the authorization code.
        """
        if not code:
            raise InvalidAuthorizationCode()
        self._add_authorize_code(code)

        token_req: RequestsResponse = self._request_access_token()
        token_response: Dict[str, str] = token_req.json()

        error: Optional[str] = token_response.get("error")
        if error:
            error_description: str = token_response.get("error_description")
            raise PlatformServerException(error, error_description)

        access_token: Optional[str] = token_response.get("access_token")
        if not access_token:
            raise EmptyTokenException()

        return access_token

    def get_user_profile(self, access_token: str) -> Dict[str, str | int]:
        """
        Get user profile by the access token.
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        user_profile: RequestsResponse = requests.get(
            f"{self.oauth_request_url}?access_token={access_token}", headers=headers
        )
        response_status_code: int = user_profile.status_code

        if response_status_code != 200:
            error_description = "Failed to retrieve user profile The access token may be invalid or expired."
            raise PlatformServerException(response_status_code, error_description)

        return user_profile.json()

    def get_username(self, user_profile: Dict[str, str | Dict]) -> str:
        """
        Get user username by the user profile.
        """
        username = user_profile.get("name")

        if not username:
            uuid = self.get_user_uuid(user_profile)[:4]
            return f"Unkown{uuid}"
        return username

    def get_user_uuid(self, user_profile: Dict[str, str | int]) -> str:
        """
        Get user uuid by the user profile.
        """
        uuid: Optional[str] = user_profile.get(self.uuid_key)

        if not uuid:
            raise ValueError("user_id is not found into user profile")
        return str(uuid)

    def social_login(self, user: SocialUser) -> Response:
        """
        Login a social user.
        """
        refresh: RefreshToken = RefreshToken.for_user(user)
        access_token_lifetime: timedelta = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
        refresh_token_lifetime: timedelta = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]

        data = {"detail": "successfully logged in"}
        response: Response = Response(data, status=status.HTTP_200_OK)

        # NOTE: remove sametime option -> use default to possible different sites receive cookies
        response.set_cookie("access_token", str(refresh.access_token), max_age=access_token_lifetime)
        response.set_cookie("refresh_token", str(refresh), httponly=True, max_age=refresh_token_lifetime)
        update_last_login(None, user)  # NOTE: update social user last login field

        return response

    def social_logout(self) -> Response:
        response = Response({"message": "Success Logout"}, status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response

    def register(self, user_profile: Dict[str, str | int]) -> Response:
        """
        Register a new social user and redirect login method.
        """
        username = self.get_username(user_profile)

        user: SocialUser = SocialUser.objects.create(
            uuid=self.get_user_uuid(user_profile),
            username=username,
            provider=self.platform,
        )
        return self.social_login(user)
