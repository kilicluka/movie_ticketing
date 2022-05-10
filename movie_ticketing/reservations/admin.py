from core.admin import CoreAdminMixin
from django.contrib import admin

from .models import Hall, Reservation, ReservationSeat, Seat, Showtime


@admin.register(Hall)
class HallAdmin(CoreAdminMixin, admin.ModelAdmin):
    list_display = ["hall_number", "created_at", "updated_at"]
    search_fields = ["hall_number"]


@admin.register(Reservation)
class ReservationAdmin(CoreAdminMixin, admin.ModelAdmin):
    list_display = [
        "user",
        "showtime",
        "expires_at",
        "status",
        "created_at",
        "updated_at",
    ]
    search_fields = ["user__email"]


@admin.register(ReservationSeat)
class ReservationSeatAdmin(CoreAdminMixin, admin.ModelAdmin):
    list_display = ["reservation", "seat", "created_at", "updated_at"]
    search_fields = ["reservation__user__email"]


@admin.register(Seat)
class SeatAdmin(CoreAdminMixin, admin.ModelAdmin):
    list_display = [
        "hall",
        "row_identifier",
        "seat_identifier",
        "created_at",
        "updated_at",
    ]
    search_fields = ["row_identifier", "seat_identifier"]


@admin.register(Showtime)
class ShowtimeAdmin(CoreAdminMixin, admin.ModelAdmin):
    list_display = [
        "hall",
        "movie",
        "time_showing",
        "movie_format",
        "created_at",
        "updated_at",
    ]
    search_fields = ["movie__title"]
