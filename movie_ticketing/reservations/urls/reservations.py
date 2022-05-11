from django.urls import path
from reservations.views import ReservationsView

urlpatterns = [
    path("", ReservationsView.as_view(), name="reservations"),
]
