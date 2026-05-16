from rest_framework import serializers

from .models import Coach, CoachAvailability


class CoachAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachAvailability
        fields = "__all__"
        read_only_fields = ("academy", "coach")


class CoachSerializer(serializers.ModelSerializer):
    availabilities = CoachAvailabilitySerializer(many=True, read_only=True)
    user_name = serializers.CharField(source="user.get_full_name", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Coach
        fields = "__all__"
        read_only_fields = ("academy",)
