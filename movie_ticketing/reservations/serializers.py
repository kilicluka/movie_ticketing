from datetime import timedelta

from django.db.models import Exists, OuterRef
from django.utils import timezone
from movies.serializers import MovieSerializer
from rest_framework import serializers

from .choices import ReservationStatus
from .models import Hall, Reservation, ReservationSeat, Seat, Showtime


class ReservationsSerializer(serializers.ModelSerializer):
    seat_uuid = serializers.UUIDField(required=True)
    showtime_uuid = serializers.UUIDField(required=True)

    class Meta:
        model = Reservation
        fields = ["user", "seat_uuid", "showtime_uuid"]

    def validate_showtime_uuid(self, value):
        try:
            showtime = Showtime.objects.get(uuid=value)
            if self._is_reservation_on_time(showtime):
                return value
            raise serializers.ValidationError(
                {"non_field_error": "Reservation period has passed."}
            )
        except Showtime.DoesNotExist:
            raise serializers.ValidationError(
                {"showtime_uuid": "Showtime with the provided uuid does not exist."}
            )

    def _is_reservation_on_time(self, showtime):
        return (
            timezone.now()
            + timedelta(minutes=Reservation.MINUTES_BEFORE_MOVIE_DEADLINE)
            <= showtime.time_showing
        )

    def validate(self, attrs):
        attrs["showtime"] = Showtime.objects.get(uuid=attrs.pop("showtime_uuid"))
        self._check_open_reservation_does_not_exist(attrs["user"], attrs["showtime"])
        attrs["seat"] = self._get_seat_if_available(
            attrs.pop("seat_uuid"), attrs["showtime"]
        )
        return attrs

    def _check_open_reservation_does_not_exist(self, user, showtime):
        if Reservation.objects.filter(
            user=user,
            showtime=showtime,
            status=ReservationStatus.OPEN,
        ).exists():
            raise serializers.ValidationError(
                {
                    "non_field_error": (
                        "You already have an open reservation for this show."
                    )
                }
            )

    def _get_seat_if_available(self, seat_uuid, showtime):
        try:
            seat = Seat.objects.get(uuid=seat_uuid, hall=showtime.hall)
            if seat.is_available_for_showtime(showtime):
                return seat
            raise serializers.ValidationError(
                {"seat_uuid": "That seat is not available."}
            )
        except Seat.DoesNotExist:
            raise serializers.ValidationError({"seat_uuid": "Invalid seat selected."})

    def create(self, validated_data):
        seat = validated_data.pop("seat")
        reservation = Reservation.objects.create(
            **validated_data,
            expires_at=timezone.now()
            + timedelta(minutes=Reservation.MINUTES_BEFORE_EXPIRY),
        )
        reservation.add_seat(seat)
        return reservation

    def to_representation(self, instance):
        return {
            "reservation_uuid": str(instance.uuid),
            "showtime_uuid": str(instance.showtime.uuid),
            "status": instance.status,
            "expires_at": instance.expires_at,
            "seats": [SeatSerializer(seat).data for seat in instance.seats.all()],
        }


class SeatSerializer(serializers.ModelSerializer):
    is_available = serializers.BooleanField(required=False)

    class Meta:
        model = Seat
        fields = ["uuid", "row_identifier", "seat_identifier", "is_available"]


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ["uuid", "hall_number"]


class ShowtimesSerializer(serializers.ModelSerializer):
    hall_uuid = serializers.UUIDField(source="hall.uuid")
    movie = MovieSerializer()

    class Meta:
        model = Showtime
        fields = ["uuid", "hall_uuid", "movie", "time_showing", "movie_format"]


class ShowtimeDetailSerializer(serializers.ModelSerializer):
    hall = HallSerializer()
    movie = MovieSerializer()
    seats = serializers.SerializerMethodField()

    class Meta:
        model = Showtime
        fields = ["uuid", "movie", "time_showing", "movie_format", "hall", "seats"]

    @staticmethod
    def get_seats(showtime):
        seats = Seat.objects.filter(hall=showtime.hall).annotate(
            is_available=Exists(
                queryset=ReservationSeat.objects.filter(
                    seat__pk=OuterRef("pk"), reservation__showtime=showtime
                ),
                negated=True,
            )
        )
        return SeatSerializer(seats, many=True).data
