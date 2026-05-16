from rest_framework import serializers

from .models import CancellationPolicy, CancellationRequest


class CancellationPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = CancellationPolicy
        fields = "__all__"
        read_only_fields = ("academy",)


class CancellationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CancellationRequest
        fields = "__all__"
        read_only_fields = ("academy", "status", "request_date", "reviewed_by", "review_notes")
