from rest_framework import serializers

from .models import BookingRequest


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookingRequest

        fields = [
            "id",
            "parent",
            "lsa",
            "start_time",
            "end_time",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "created_at",
        ]

    def validate(self, data):

        if data["start_time"] >= data["end_time"]:
            raise serializers.ValidationError(
                "End time must be after start time."
            )

        return data