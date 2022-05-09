from rest_framework import serializers

from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Set password.",
    )
    password_repeated = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Confirm password.",
    )

    class Meta:
        model = UserProfile
        fields = ["uuid", "email", "password", "password_repeated"]
        extra_kwargs = {"uuid": {"read_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["password_repeated"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_repeated")
        return UserProfile.objects.create_user(**validated_data)
