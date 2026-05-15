from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    primary_academy_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "phone_number", "roles", "primary_academy_id")
        read_only_fields = ("id",)

    def get_roles(self, obj):
        return list(obj.user_roles.values_list('role__name', flat=True).distinct())

    def get_primary_academy_id(self, obj):
        first_role = obj.user_roles.first()
        if first_role and first_role.academy_id:
            return str(first_role.academy_id)
        return None


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name", "phone_number")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
