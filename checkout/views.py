from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsCustomer
from .serializers import CheckoutSerializer
from .services import CheckoutService


class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "message": "Checkout validation failed.",
                    "data": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            checkout_data = CheckoutService.checkout(
                customer=request.user,
                fulfillment_mode=serializer.validated_data["fulfillment_mode"],
                payment_type=serializer.validated_data["payment_type"],
            )
        except ValidationError as e:
            return Response(
                {
                    "success": False,
                    "message": e.messages[0],
                    "data": None
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
                "success": True,
                "message": "Checkout validated successfully.",
                "data": {
                    "cart_id": checkout_data["cart"].id,
                    "store": {"id": checkout_data["store"].id,"name": checkout_data["store"].store_name,},
                    "fulfillment_mode": checkout_data["fulfillment_mode"],
                    "payment_type": checkout_data["payment_type"],
                    "items": checkout_data["items"],
                    "cart_total": checkout_data["cart_total"],
                    }
            },
            status=status.HTTP_200_OK)
    
    