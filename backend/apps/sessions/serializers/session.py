from rest_framework import serializers

from ..models import Enrollment, ScheduleConflict, SessionCoach, SessionOccurrence, SessionSeries, Venue


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = "__all__"


class SessionSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionSeries
        fields = "__all__"
        read_only_fields = ("academy",)


class SessionOccurrenceSerializer(serializers.ModelSerializer):
    series = SessionSeriesSerializer(read_only=True)
    venue = VenueSerializer(read_only=True)

    class Meta:
        model = SessionOccurrence
        fields = "__all__"
        read_only_fields = ("academy",)


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = "__all__"
        read_only_fields = ("academy",)


class SessionCoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionCoach
        fields = "__all__"
        read_only_fields = ("academy",)


class ScheduleConflictSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleConflict
        fields = "__all__"
        read_only_fields = ("academy",)
