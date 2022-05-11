from django.urls import path
from reservations.views import ShowtimeDetailView, ShowtimesView

urlpatterns = [
    path("", ShowtimesView.as_view(), name="showtimes"),
    path("<uuid:uuid>/", ShowtimeDetailView.as_view(), name="showtime-detail"),
]
