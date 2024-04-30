from dataclasses import asdict, dataclass
from typing import Optional

from django.conf import settings


@dataclass
class Secret:
    client_id: str
    redirect_uri: str
    token_info_api: str
    client_secret: Optional[str] = None
    state: Optional[str] = None

    def to_dict(self):
        return asdict(self)


@dataclass
class GoogleAuth:
    info = Secret(**settings.SOCIAL_PLATFORM.get("google"))


@dataclass
class KakaoAuth:
    info = Secret(**settings.SOCIAL_PLATFORM.get("kakao"))


@dataclass
class GithubAuth:
    info = Secret(**settings.SOCIAL_PLATFORM.get("github"))


@dataclass
class SocialPlatform:
    """
    Social platform domain with authentication values.
    """

    google: GoogleAuth = GoogleAuth
    kakao: KakaoAuth = KakaoAuth
    github: GithubAuth = GithubAuth


@dataclass
class PlatformRequestUrl:
    """
    Platform service server request endpoint.
    """

    google: str = settings.PLATFORM_URL.get("google").get("url")
    kakao: str = settings.PLATFORM_URL.get("kakao").get("url")
    github: str = settings.PLATFORM_URL.get("github").get("url")
