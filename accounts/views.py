from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .services import *
from .permissions import *
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterAPIView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                    "success": True,
                    "message": "User registered successfully.",
                    "data": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "role": user.role,
                    }
                },status=status.HTTP_201_CREATED
            )
        return Response({
                "success": False,
                "message": "Registration failed.",
                "data": serializer.errors
            },status=status.HTTP_400_BAD_REQUEST
        )
    
class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        return Response(
            {
                "success": True,
                "message": "Login successful.",
                "data": response.data
            },
            status=status.HTTP_200_OK
        )

class StaffRegistrationAPIView(APIView):

    def post(self, request):

        serializer = StaffRegistrationSerializer(data=request.data)

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "message": "Staff registration request failed.",
                    "data": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            registration_request = (
                StaffRegistrationService
                .create_registration_request(
                    serializer.validated_data
                )
            )

        except ValidationError as error:

            return Response(
                {
                    "success": False,
                    "message": "Staff registration request failed.",
                    "data": error.detail
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message": (
                    "Staff registration request submitted "
                    "successfully. Waiting for approval."
                ),
                "data": {
                    "request_id": registration_request.id,
                    "username": registration_request.username,
                    "role": registration_request.requested_role,
                    "requested_store": (
                        registration_request
                        .requested_store
                        .store_code
                    ),
                    "status": registration_request.status,
                }
            },
            status=status.HTTP_201_CREATED
        )

class StaffRegistrationApprovalAPIView(APIView):

    permission_classes = [IsSupervisorOrAdmin]

    def post(self, request, request_id):

        try:

            user, registration_request = (StaffRegistrationApprovalService.approve_request(
                    request_id=request_id,
                    approved_by=request.user,
                )
            )

        except ValidationError as error:

            return Response(
                {
                    "success": False,
                    "message": "Staff registration approval failed.",
                    "data": error.detail,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "success": True,
                "message": "Staff registration request approved successfully.",
                "data": {
                    "request_id": registration_request.id,
                    "username": user.username,
                    "role": user.role,
                    "store": user.store.store_code,
                    "status": registration_request.status,
                },
            },
            status=status.HTTP_200_OK,
        )

class StaffRegistrationRequestListAPIView(APIView):

    permission_classes = [IsSupervisorOrAdmin]

    def get(self, request):

        requests = (StaffRegistrationApprovalListService.get_pending_requests())

        serializer = StaffRegistrationRequestSerializer(requests,many=True)

        return Response(
            {
                "success": True,
                "message": "Pending staff registration requests retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK
        )