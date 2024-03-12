# accounts/serializers.py
from rest_framework import serializers
from .models import CustomUser, Role


class UserSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source="role.name", read_only=True)
    updated_profile = serializers.BooleanField(read_only=True)

    class Meta:
        model = CustomUser
        exclude = ["password", "user_permissions"]
        # depth = 2


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # exclude = ('groups', 'user_permissions', "client", "is_staff", "is_superuser", "date_joined", "role")
        fields = [
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "role",
        ]

    def create(self, validated_data):
        role = validated_data.get("role", "Passenger")
        user = CustomUser.objects.create(
            **validated_data, role=role, is_staff=False, is_superuser=False
        )
        return user


class CustomUserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ("groups", "user_permissions", "password")


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ("password",)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class CustomRegisterSerializer(serializers.ModelSerializer):
    role = serializers.CharField(max_length=255)

    class Meta:
        model = CustomUser
        fields = ["role", "email", "username", "password"]
