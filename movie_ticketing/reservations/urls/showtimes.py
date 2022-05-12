from django.urls import path
from reservations.views import ShowtimesView, ShowtimeView

urlpatterns = [
    path("", ShowtimesView.as_view(), name="showtimes"),
    path("<uuid:uuid>/", ShowtimeView.as_view(), name="showtime"),
]
