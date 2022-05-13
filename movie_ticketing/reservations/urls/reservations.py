from django.urls import path
from reservations.views import (
    CompleteReservationView,
    ReservationsView,
    ReservationView,
)

urlpatterns = [
    path("", ReservationsView.as_view(), name="reservations"),
    path("<uuid:uuid>/", ReservationView.as_view(), name="reservation"),
    path(
        "<uuid:uuid>/complete/",
        CompleteReservationView.as_view(),
        name="complete-reservation",
    ),
]
