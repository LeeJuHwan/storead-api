from django.urls import path

from . import views

urlpatterns = [
    path("me/", views.MyProfileDetailAPIView.as_view(), name="my-profile"),
    path("me/update/", views.UpdateProfileAPIView.as_view(), name="update-profile"),
    path("me/following/", views.FollowingListView.as_view(), name="following"),
    path("me/followers/", views.FollowerListView.as_view(), name="followers"),
    path(
        "<uuid:profile_id>/",
        views.UserProfileDetailAPIView.as_view(),
        name="user-profile",
    ),
    path("<str:user_id>/follow/", views.FollowAPIView.as_view(), name="follow"),
    path("<str:user_id>/unfollow/", views.UnfollowAPIView.as_view(), name="unfollow"),
]
