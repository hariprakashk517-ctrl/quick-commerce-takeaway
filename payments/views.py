from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import *
from .serializers import *
from .services import *


class CollectPaymentAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTakeawayStaffOrAdminOrSupervisor]

    def post(self, request, order_id):
        serializer = CollectPaymentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "message": "Payment validation failed.",
                    "data": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            payment = PaymentService.collect_payment(
                order_id=order_id,
                payment_type=serializer.validated_data["payment_type"],
                transaction_id=serializer.validated_data.get("transaction_id",""),
                collected_by=request.user,
            )
        except ValidationError as error:
            return Response(
                {
                    "success": False,
                    "message": error.messages[0],
                    "data": None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "success": True,
                "message": "Payment collected successfully.",
                "data": {
                    "order_id": payment.order.order_id,
                    "payment_type": payment.payment_type,
                    "payment_status": payment.status,
                    "amount": payment.amount,
                    "transaction_id": payment.transaction_id,
                    "paid_at": payment.paid_at,
                    "order_status": payment.order.order_status,
                },
            },
            status=status.HTTP_200_OK,
        )
    
class CashHandoverAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSupervisorOrAdmin]

    def post(self, request, order_id):
        serializer = CashHandoverSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                    "success": False,
                    "message": "Cash handover validation failed.",
                    "data": serializer.errors,
                },status=status.HTTP_400_BAD_REQUEST,)

        try:
            cash_ledger = PaymentService.handover_cash(
            order_id=order_id,
            supervisor=request.user,
            supervisor_note=serializer.validated_data.get("supervisor_note","",),)
        except ValidationError as error:
            return Response({
                    "success": False,
                    "message": error.messages[0],
                    "data": None,
                },status=status.HTTP_400_BAD_REQUEST,)

        return Response({
                "success": True,
                "message": "Cash handed over successfully.",
                "data": {
                    "payment_id": cash_ledger.payment.id,
                    "amount": cash_ledger.amount,
                    "status": cash_ledger.status,
                    "handed_over_to": cash_ledger.handed_over_to.id,
                    "handed_over_at": cash_ledger.handed_over_at,
                    "supervisor_note": cash_ledger.supervisor_note,
                },
            },status=status.HTTP_200_OK,)