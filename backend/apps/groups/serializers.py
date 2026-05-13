from rest_framework import serializers

from .models import Group, GroupCoach


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
        read_only_fields = ("academy",)


class GroupCoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupCoach
        fields = "__all__"
        read_only_fields = ("academy",)
