from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import UserProfileSerializer


class UserProfileCreateView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]
