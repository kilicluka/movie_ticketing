from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Reservation, Showtime
from .serializers import (
    ReservationSerializer,
    ReservationsSerializer,
    ShowtimeSerializer,
    ShowtimesSerializer,
)


class ReservationsView(generics.ListCreateAPIView):
    serializer_class = ReservationsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Reservation.objects.filter(user=self.request.user)
            .prefetch_related("seats")
            .select_related("showtime", "showtime__movie")
        )

    def post(self, request, *args, **kwargs):
        request.data.update({"user": request.user.pk})
        return super().create(request, *args, **kwargs)


class ReservationView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"

    def get_queryset(self):
        return (
            Reservation.objects.filter(user=self.request.user)
            .prefetch_related("seats")
            .select_related("showtime", "showtime__movie")
        )

    def patch(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ShowtimesView(generics.ListAPIView):
    serializer_class = ShowtimesSerializer
    permission_classes = [AllowAny]
    queryset = Showtime.objects.showing().select_related("movie", "hall")


class ShowtimeView(generics.RetrieveAPIView):
    serializer_class = ShowtimeSerializer
    permission_classes = [AllowAny]
    lookup_field = "uuid"
    queryset = (
        Showtime.objects.showing()
        .select_related("movie", "hall")
        .prefetch_related("hall__seats")
    )
