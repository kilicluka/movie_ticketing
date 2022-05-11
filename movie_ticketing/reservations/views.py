from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Reservation, Showtime
from .serializers import ReservationsSerializer, ShowtimesSerializer


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


class ShowtimesView(generics.ListAPIView):
    serializer_class = ShowtimesSerializer
    permission_classes = [AllowAny]
    queryset = Showtime.objects.available().select_related("movie", "hall")
