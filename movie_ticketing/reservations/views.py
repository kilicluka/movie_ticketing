from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Reservation
from .serializers import ReservationsSerializer


class ReservationsView(generics.ListCreateAPIView):
    serializer_class = ReservationsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).prefetch_related(
            "seats"
        )

    def post(self, request, *args, **kwargs):
        request.data.update({"user": request.user.pk})
        return super().create(request, *args, **kwargs)
