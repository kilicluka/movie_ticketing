from string import ascii_uppercase

from core.models import BaseModel
from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

from .choices import MovieFormat, ReservationStatus
from .managers import ShowtimeManager


class Reservation(BaseModel):
    MINUTES_BEFORE_MOVIE_DEADLINE = 30
    MINUTES_BEFORE_EXPIRY = 15

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="reservations",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        help_text=_("User who made the reservation."),
    )
    showtime = models.ForeignKey(
        to="reservations.Showtime",
        related_name="reservations",
        on_delete=models.CASCADE,
        verbose_name=_("Showtime"),
        help_text=_("Showtime for which the reservation was created."),
    )
    seats = models.ManyToManyField(
        to="reservations.Seat",
        through="reservations.ReservationSeat",
        related_name="reservations",
        verbose_name=_("Seats"),
        help_text=_("Seats reserved with this reservation."),
    )
    status = models.CharField(
        choices=ReservationStatus.choices,
        default=ReservationStatus.OPEN,
        max_length=9,
        verbose_name=_("Status"),
        help_text=_("Reservation's current status."),
    )
    expires_at = models.DateTimeField(
        verbose_name=_("Expires At"),
        help_text=_("When does the reservation expire if it hasn't been completed."),
    )

    class Meta:
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")
        db_table = "reservation"

    def __str__(self):
        return f"{self.user.email} - {self.showtime}"

    def add_seat(self, seat):
        return ReservationSeat.objects.create(reservation=self, seat=seat)


class Seat(BaseModel):
    hall = models.ForeignKey(
        to="reservations.Hall",
        related_name="seats",
        on_delete=models.CASCADE,
        verbose_name=_("Hall"),
        help_text=_("Hall where the seat is located."),
    )
    row_identifier = models.CharField(
        choices=list(zip(ascii_uppercase, ascii_uppercase)),
        max_length=1,
        verbose_name=_("Row Identifier"),
        help_text=_("Identifier of the row the seat belongs to."),
    )
    seat_identifier = models.CharField(
        choices=list(map(lambda x: (str(x), str(x)), range(1, 100))),
        max_length=2,
        verbose_name=_("Seat Identifier"),
        help_text=_("Identifier of the seat in the row."),
    )

    class Meta:
        verbose_name = _("Seat")
        verbose_name_plural = _("Seats")
        db_table = "seat"
        unique_together = ("hall", "row_identifier", "seat_identifier")

    def __str__(self):
        return f"{str(self.hall)} - {self.row_identifier}{self.seat_identifier}"

    def is_available_for_showtime(self, showtime):
        return not ReservationSeat.objects.filter(
            seat=self, reservation__showtime=showtime
        ).exists()


class ReservationSeat(BaseModel):
    reservation = models.ForeignKey(
        to="reservations.Reservation",
        related_name="reservation_seats",
        on_delete=models.CASCADE,
        verbose_name=_("Reservation"),
        help_text=_("Reservation which the seat belongs to."),
    )
    seat = models.ForeignKey(
        to="reservations.Seat",
        related_name="reservation_seats",
        on_delete=models.CASCADE,
        verbose_name=_("Seat"),
        help_text=_("Seat which is reserved."),
    )

    class Meta:
        verbose_name = _("Reservation Seat")
        verbose_name_plural = _("Reservation Seats")
        db_table = "reservation_seat"

    def __str__(self):
        return f"{self.reservation} - {self.seat}"


class Showtime(BaseModel):
    hall = models.ForeignKey(
        to="reservations.Hall",
        related_name="showtimes",
        on_delete=models.CASCADE,
        verbose_name=_("Hall"),
        help_text=_("Hall where the movie is showing."),
    )
    movie = models.ForeignKey(
        to="movies.Movie",
        related_name="showtimes",
        on_delete=models.CASCADE,
        verbose_name=_("Movie"),
        help_text=_("Movie that is showing."),
    )
    time_showing = models.DateTimeField(
        verbose_name=_("Time Showing"),
        help_text=_("When is the movie showing."),
    )
    movie_format = models.CharField(
        choices=MovieFormat.choices,
        default=MovieFormat.TWO_D,
        max_length=3,
        verbose_name=_("Movie Format"),
        help_text=_("Format in which the movie is showing."),
    )

    objects = ShowtimeManager()

    class Meta:
        verbose_name = _("Showtime")
        verbose_name_plural = _("Showtimes")
        db_table = "showtime"

    def __str__(self):
        return (
            f"{self.movie} ({self.movie_format}) - "
            f"{self.hall}: {self.time_showing.strftime(settings.DATETIME_FORMAT)}"
        )


class Hall(BaseModel):
    hall_number = models.SmallIntegerField(
        verbose_name=_("Hall Number"),
        help_text=_("Number of the movie hall."),
    )

    class Meta:
        verbose_name = _("Hall")
        verbose_name_plural = _("Halls")
        db_table = "hall"

    def __str__(self):
        return f"H{self.hall_number}"
