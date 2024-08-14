from django.urls import path

from . import views

urlpatterns = [
    path("/me", views.MyProfileDetailAPI.as_view(), name="my-profile"),
    path("/me/update", views.UpdateProfileAPI.as_view(), name="update-profile"),
    path("/me/following", views.MyFollowingListAPI.as_view(), name="my-following"),
    path("/me/followers", views.MyFollowerListAPI.as_view(), name="my-followers"),
    path("/<uuid:profile_id>/following", views.UserFollowingListAPI.as_view(), name="user-following"),
    path("/<uuid:profile_id>/followers", views.UserFollowerListAPI.as_view(), name="user-followers"),
    path(
        "/<uuid:profile_id>",
        views.UserProfileDetailAPI.as_view(),
        name="user-profile",
    ),
    path("/<str:user_id>/follow", views.FollowAPI.as_view(), name="follow"),
    path("/<str:user_id>/unfollow", views.UnfollowAPI.as_view(), name="unfollow"),
]
