from django.urls import path

from .views import ReservationsView

urlpatterns = [
    path("", ReservationsView.as_view(), name="reservations"),
]
