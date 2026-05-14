from rest_framework import serializers

from ..models import Enrollment, SessionOccurrence, SessionSeries, Venue


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
    title = serializers.CharField(source='series.title', read_only=True)
    venue_name = serializers.CharField(source='venue.name', read_only=True)
    
    class Meta:
        model = SessionOccurrence
        fields = "__all__"
        read_only_fields = ("academy",)


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = "__all__"
        read_only_fields = ("academy",)
