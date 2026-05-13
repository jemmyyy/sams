from rest_framework import serializers

from .models import CancellationRequest


class CancellationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CancellationRequest
        fields = "__all__"
        read_only_fields = ("academy", "player", "status", "request_date")
