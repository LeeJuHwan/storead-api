from django.urls import path
from . import views


urlpatterns = [
    path("connections/google/", views.GoogleLogin.as_view(), name="google_login"),
    path("connections/kakao/", views.KakaoLogin.as_view(), name="kakao_login"),
    path("connections/github/", views.GithubLogin.as_view(), name="github_login"),
]
