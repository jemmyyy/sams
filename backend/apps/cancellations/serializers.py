from rest_framework import serializers

from .models import CancellationRequest


class CancellationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CancellationRequest
        fields = "__all__"
        read_only_fields = ("academy", "status", "request_date", "reviewed_by", "review_notes")
