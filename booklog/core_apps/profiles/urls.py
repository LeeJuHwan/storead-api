from django.urls import path

from . import views

urlpatterns = [
    path("me/", views.ProfileDetailAPIView.as_view(), name="my-profile"),
]
