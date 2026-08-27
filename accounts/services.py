from django.db import transaction
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from stores.models import Store
from .models import StaffRegistrationRequest
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()

class StaffRegistrationService:

    @staticmethod
    @transaction.atomic
    def create_registration_request(validated_data):

        password = validated_data.pop("password")
        store_code = validated_data.pop("store_code")
        role = validated_data.pop("role")

        if role not in ["PACKER","TAKEAWAY_STAFF","SUPERVISOR",]:
            raise ValidationError("Invalid staff role.")

        try:
            store = Store.objects.get(store_code=store_code,is_active=True)
        except Store.DoesNotExist:
            raise ValidationError("Invalid or inactive store.")
        
        registration_request = StaffRegistrationRequest.objects.create(
            full_name=validated_data["full_name"],
            username=validated_data["username"],
            email=validated_data["email"],
            phone_number=validated_data["phone_number"],
            password_hash=make_password(password),
            requested_role=role,
            requested_store=store,
            status="PENDING",
        )

        return registration_request

class StaffRegistrationApprovalService:

    @staticmethod
    @transaction.atomic
    def approve_request(request_id, approved_by):

        try:
            registration_request = (
                StaffRegistrationRequest.objects
                .select_for_update()
                .get(id=request_id)
            )
        except StaffRegistrationRequest.DoesNotExist:
            raise ValidationError("Staff registration request not found.")

        if registration_request.status != "PENDING":
            raise ValidationError("Only pending registration requests can be approved.")

        if User.objects.filter(username=registration_request.username).exists():
            raise ValidationError("Username already exists.")

        if User.objects.filter(email=registration_request.email).exists():
            raise ValidationError("Email already exists.")

        if User.objects.filter(phone_number=registration_request.phone_number).exists():
            raise ValidationError("Phone number already exists.")

        user = User(
            username=registration_request.username,
            email=registration_request.email,
            phone_number=registration_request.phone_number,
            full_name=registration_request.full_name,
            role=registration_request.requested_role,
            store=registration_request.requested_store,
            is_active=True,
            password=registration_request.password_hash,
        )

        user.save()

        registration_request.status = "APPROVED"
        registration_request.approved_by = approved_by
        registration_request.approved_at = timezone.now()
        registration_request.save(
            update_fields=[
                "status",
                "approved_by",
                "approved_at",
                "updated_at",
            ]
        )

        return user, registration_request

class StaffRegistrationApprovalListService:

    @staticmethod
    def get_pending_requests():

        return (
            StaffRegistrationRequest.objects
            .filter(status="PENDING")
            .select_related("requested_store")
            .order_by("-created_at")
        )