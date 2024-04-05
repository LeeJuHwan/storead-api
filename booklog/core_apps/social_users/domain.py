from dataclasses import dataclass, asdict
from typing import Optional
from django.conf import settings


SOCIAL = settings.SOCIAL_PLATFORM


@dataclass
class Secret:
    client_id: str
    redirect_uri: str
    token_info_api: str
    client_secret: Optional[str] = None

    def to_dict(self):
        return asdict(self)


@dataclass
class GoogleAuth:
    info = Secret(**SOCIAL.get("google"))


@dataclass
class KakaoAuth(Secret):
    info = Secret(**SOCIAL.get("kakao"))


@dataclass
class GithubAuth(Secret):
    info = Secret(**SOCIAL.get("github"))


@dataclass
class SocialPlatform:
    google: GoogleAuth = GoogleAuth
    kakao: KakaoAuth = KakaoAuth
    github: GithubAuth = GithubAuth
