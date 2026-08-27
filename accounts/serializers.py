from rest_framework import serializers
from .models import *
from stores.models import Store
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone_number",
            "full_name",
            "role",
            "password",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user

class LoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["username"] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "full_name": self.user.full_name,
            "email": self.user.email,
            "role": self.user.role,
        }
        return data

class StaffRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=10)
    full_name = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True,min_length=8)
    role = serializers.ChoiceField(
        choices=[
            ("PACKER", "PACKER"),
            ("TAKEAWAY_STAFF", "TAKEAWAY_STAFF"),
            ("SUPERVISOR", "SUPERVISOR"),
        ]
    )

    store_code = serializers.CharField(max_length=20)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")

        if StaffRegistrationRequest.objects.filter(username=value,status="PENDING").exists():
            raise serializers.ValidationError("A registration request already exists for this username.")

        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")

        if StaffRegistrationRequest.objects.filter(email=value,status="PENDING").exists():
            raise serializers.ValidationError("A registration request already exists for this email.")

        return value

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already exists.")

        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Phone number must contain exactly 10 digits.")

        if StaffRegistrationRequest.objects.filter(phone_number=value,status="PENDING").exists():
            raise serializers.ValidationError("A registration request already exists for this phone number.")

        return value

    def validate_store_code(self, value):
        try:
            store = Store.objects.get(
                store_code=value,
                is_active=True
            )
        except Store.DoesNotExist:
            raise serializers.ValidationError("Invalid or inactive store.")

        return value

class StaffRegistrationRequestSerializer(serializers.ModelSerializer):
    request_id = serializers.IntegerField(source="id")
    role = serializers.CharField(source="requested_role")
    requested_store = serializers.CharField(source="requested_store.store_code")

    class Meta:
        model = StaffRegistrationRequest
        fields = [
            "request_id",
            "username",
            "role",
            "requested_store",
            "status",
        ]