from django.urls import path
from reservations.views import ShowtimesView

urlpatterns = [
    path("", ShowtimesView.as_view(), name="showtimes"),
]
