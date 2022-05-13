from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

UserProfile = get_user_model()


class ShowtimeManager(models.Manager):
    def showing(self):
        return self.get_queryset().filter(time_showing__gt=timezone.now())


class SeatManager(models.Manager):
    def showtime_seats(self, showtime):
        from .models import ReservationSeat

        return (
            self.get_queryset()
            .prefetch_related("hall__seats")
            .filter(hall=showtime.hall)
            .annotate(
                is_available=models.Exists(
                    queryset=ReservationSeat.objects.filter(
                        seat__pk=models.OuterRef("pk"), reservation__showtime=showtime
                    ),
                    negated=True,
                ),
            )
        )

    def user_showtime_seats(self, showtime, user):
        from .models import ReservationSeat

        return self.get_queryset().filter(
            pk__in=ReservationSeat.objects.filter(
                reservation__showtime=showtime, reservation__user=user
            ).values("seat__pk")
        )
