from datetime import timedelta

from django.utils import timezone
from movies.serializers import MovieSerializer
from rest_framework import serializers

from .choices import ReservationStatus
from .models import Hall, Reservation, Seat, Showtime


class ReservationSerializerBase(serializers.ModelSerializer):
    @staticmethod
    def check_reservations_still_accepted(showtime):
        if (
            timezone.now()
            + timedelta(minutes=Reservation.MINUTES_BEFORE_MOVIE_DEADLINE)
            > showtime.time_showing
        ):
            raise serializers.ValidationError(
                {"non_field_error": "Reservation period has passed."}
            )

    @staticmethod
    def get_seat_if_available(seat_uuid, showtime):
        try:
            seat = Seat.objects.get(uuid=seat_uuid, hall=showtime.hall)
            if seat.is_available_for_showtime(showtime):
                return seat
            raise serializers.ValidationError(
                {"seat_uuid": "That seat is not available."}
            )
        except Seat.DoesNotExist:
            raise serializers.ValidationError({"seat_uuid": "Invalid seat selected."})

    def to_representation(self, instance):
        return {
            "uuid": str(instance.uuid),
            "showtime": ShowtimesSerializer(instance.showtime).data,
            "status": instance.status,
            "expires_at": instance.expires_at,
            "seats": [SeatSerializer(seat).data for seat in instance.seats.all()],
        }


class ReservationsSerializer(ReservationSerializerBase):
    seat_uuid = serializers.UUIDField(required=True)
    showtime_uuid = serializers.UUIDField(required=True)

    class Meta:
        model = Reservation
        fields = ["user", "seat_uuid", "showtime_uuid"]

    def validate_showtime_uuid(self, value):
        try:
            showtime = Showtime.objects.get(uuid=value)
            self.check_reservations_still_accepted(showtime)
            return value
        except Showtime.DoesNotExist:
            raise serializers.ValidationError(
                {"showtime_uuid": "Showtime with the provided uuid does not exist."}
            )

    def validate(self, attrs):
        attrs["showtime"] = Showtime.objects.get(uuid=attrs.pop("showtime_uuid"))
        self._check_open_reservation_does_not_exist(attrs["user"], attrs["showtime"])
        attrs["seat"] = self.get_seat_if_available(
            attrs.pop("seat_uuid"), attrs["showtime"]
        )
        return attrs

    @staticmethod
    def _check_open_reservation_does_not_exist(user, showtime):
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

    def create(self, validated_data):
        seat = validated_data.pop("seat")
        reservation = Reservation.objects.create(
            **validated_data,
            expires_at=timezone.now()
            + timedelta(minutes=Reservation.MINUTES_BEFORE_EXPIRY),
        )
        reservation.add_seat(seat)
        return reservation


class ReservationSerializer(ReservationSerializerBase):
    seat_uuid = serializers.UUIDField()

    class Meta:
        model = Reservation
        fields = ["seat_uuid"]

    def update(self, instance, validated_data):
        if not validated_data.get("seat_uuid"):
            raise serializers.ValidationError({"seat_uuid": "This field is required."})

        self.check_reservations_still_accepted(instance.showtime)
        if instance.status == ReservationStatus.COMPLETED:
            raise serializers.ValidationError(
                {"non_field_error": "Reservation is not OPEN."}
            )
        seat = self.get_seat_if_available(
            validated_data["seat_uuid"], instance.showtime
        )
        instance.add_seat(seat)
        return instance


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
    hall = HallSerializer()
    movie = MovieSerializer()

    class Meta:
        model = Showtime
        fields = ["uuid", "hall", "movie", "time_showing", "movie_format"]


class ShowtimeSerializer(serializers.ModelSerializer):
    hall = HallSerializer()
    movie = MovieSerializer()
    seats = serializers.SerializerMethodField()

    class Meta:
        model = Showtime
        fields = ["uuid", "movie", "time_showing", "movie_format", "hall", "seats"]

    @staticmethod
    def get_seats(showtime):
        seats = Seat.objects.showtime_seats(showtime)
        return SeatSerializer(seats, many=True).data
