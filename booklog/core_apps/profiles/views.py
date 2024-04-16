from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import ProfileSerializer
from .models import Profile
from .renderers import ProfileJSONRenderer


class ProfileDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    renderer_classes = [ProfileJSONRenderer]

    def get_queryset(self):
        queryset = Profile.objects.select_related("user")  # NOTE: relationship table ORM
        return queryset

    def get_object(self):
        user = self.request.user
        profile = self.get_queryset().first()
        return profile
