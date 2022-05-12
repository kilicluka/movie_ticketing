from django.urls import path
from reservations.views import ReservationsView, ReservationView

urlpatterns = [
    path("", ReservationsView.as_view(), name="reservations"),
    path("<uuid:uuid>/", ReservationView.as_view(), name="reservation"),
]
