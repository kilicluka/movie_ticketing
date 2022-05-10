from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import ReservationsSerializer


class ReservationsView(generics.ListCreateAPIView):
    serializer_class = ReservationsSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.data.update({"user": request.user.pk})
        return super().create(request, *args, **kwargs)
