from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import * 
from .serializers import *
from .services import OrderService


class CreateOrderAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Order creation validation failed.",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = OrderService.create_order(
                customer=request.user,
                payment_type=serializer.validated_data["payment_type"],
                fulfillment_mode=serializer.validated_data["fulfillment_mode"],
            )
        except ValidationError as e:
            return Response({
                "success": False,
                "message": e.messages[0],
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "message": "Order created successfully.",
            "data": {
                "order_id": order.order_id,
                "status": order.order_status,
                "payment_status": order.payment_status,
                "total_amount": order.total_amount,
            }
        }, status=status.HTTP_201_CREATED)
    
class CustomerOrderListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request):
        orders = OrderService.list_customer_orders(request.user)
        serializer = OrderListSerializer(orders, many=True)

        return Response({
            "success": True,
            "message": "Orders fetched successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class CustomerOrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request, order_id):
        order = OrderService.get_customer_order(
            request.user,
            order_id
        )

        if order is None:
            return Response({
                "success": False,
                "message": "Order not found.",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderDetailSerializer(order)

        return Response({
            "success": True,
            "message": "Order fetched successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
class PackingOrderListAPIView(APIView):
    permission_classes = [IsAuthenticated,IsPackerOrAdminOrSupervisor]

    def get(self, request):
        orders = OrderService.list_packing_orders()
        serializer = OrderDetailSerializer(orders, many=True)

        return Response({
            "success": True,
            "message": "Packing orders fetched successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
class StartPackingAPIView(APIView):
    permission_classes = [IsAuthenticated,IsPackerOrAdminOrSupervisor]

    def post(self, request, order_id):

        try:
            order = OrderService.start_packing(
                order_id,
                request.user
            )
        except ValidationError as e:
            return Response({
                "success": False,
                "message": e.messages[0],
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderDetailSerializer(order)

        return Response({
            "success": True,
            "message": "Packing started successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
class CompletePackingAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsPackerOrAdminOrSupervisor,
    ]

    def post(self, request, order_id):
        try:
            order = OrderService.complete_packing(
                order_id,
                request.user
            )
        except ValidationError as e:
            return Response({
                "success": False,
                "message": e.messages[0],
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "message": "Packing completed successfully.",
            "data": {
                "order_id": order.order_id,
                "status": order.order_status
            }
        }, status=status.HTTP_200_OK)
    
class MarkOutForPickupAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTakeawayStaffOrAdminOrSupervisor]

    def post(self, request, order_id):
        try:
            order = OrderService.mark_out_for_pickup(order_id)
        except ValidationError as e:
            return Response({
                "success": False,
                "message": e.messages[0],
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "message": "Order moved out for pickup successfully.",
            "data": {
                "order_id": order.order_id,
                "status": order.order_status,
                "qr_expires_at": order.qr_expires_at,
                "otp_expires_at": order.otp_expires_at,
            }
        }, status=status.HTTP_200_OK)
    
class RefreshPickupCredentialsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request, order_id):
        try:
            order = OrderService.refresh_pickup_credentials(
                order_id=order_id,
                customer=request.user
            )
        except ValidationError as e:
            return Response({
                "success": False,
                "message": e.messages[0],
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "message": "Pickup credentials refreshed successfully.",
            "data": {
                "order_id": order.order_id,
                "qr_expires_at": order.qr_expires_at,
                "otp_expires_at": order.otp_expires_at,
            }
        }, status=status.HTTP_200_OK)
    
class ScanQRAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTakeawayStaffOrAdminOrSupervisor]

    def post(self, request):
        qr_token = request.data.get("qr_token")

        if not qr_token:
            return Response({
                "success": False,
                "message": "QR token is required.",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = OrderService.scan_qr(
                qr_token=qr_token,
                staff=request.user
            )
        except ValidationError as e:
            return Response({
                "success": False,
                "message": e.messages[0],
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "message": "QR scanned successfully.",
            "data": {
                "order_id": order.order_id,
                "status": order.order_status,
                "qr_scanned": order.qr_scanned,
                "otp_enabled": order.otp_enabled,
                # "next_step": "SHOW_ORDER_ITEMS"
            }
        }, status=status.HTTP_200_OK)
    
class PickupCredentialsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request, order_id):
        try:
            order = OrderService.get_pickup_credentials(
                order_id=order_id,
                customer=request.user
            )
        except ValidationError as e:
            return Response({
                "success": False,
                "message": e.messages[0],
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "message": "Pickup credentials fetched successfully.",
            "data": {
                "order_id": order.order_id,
                "qr_token": order.qr_token,
                "otp": order.otp,
                "qr_expires_at": order.qr_expires_at,
                "otp_expires_at": order.otp_expires_at,
                "qr_scanned": order.qr_scanned,
                "otp_enabled": order.otp_enabled,
            }
        }, status=status.HTTP_200_OK)
    
class OrderVerificationDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTakeawayStaffOrAdminOrSupervisor]

    def get(self, request, order_id):
        try:
            order = OrderService.get_order_for_verification(order_id)
        except ValidationError as e:
            return Response({
                "success": False,
                "message": e.messages[0],
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderVerificationSerializer(order)

        return Response({
            "success": True,
            "message": "Order ready for verification.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
class VerifyOrderItemAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTakeawayStaffOrAdminOrSupervisor]

    def post(self, request, order_id, item_id):
        try:
            item = OrderService.verify_order_item(
                order_id=order_id,
                item_id=item_id
            )
        except ValidationError as e:
            return Response({
                "success": False,
                "message": e.messages[0],
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "message": "Item verified successfully.",
            "data": {
                "item_id": item.id,
                "product_name": item.product.product_name,
                "is_verified": item.is_verified
            }
        }, status=status.HTTP_200_OK)
    
class CompleteItemVerificationAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTakeawayStaffOrAdminOrSupervisor]

    def post(self, request, order_id):
        try:
            order = OrderService.complete_item_verification(order_id)
        except ValidationError as e:
            return Response({
                "success": False,
                "message": e.messages[0],
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "message": "Item verification completed successfully.",
            "data": {
                "order_id": order.order_id,
                "status": order.order_status,
                "verification_completed": order.verification_completed,
                "payment_status": order.payment_status
            }
        }, status=status.HTTP_200_OK)
    
class CancelOrderItemAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTakeawayStaffOrAdminOrSupervisor]

    def post(self, request, order_id, item_id):
        serializer = CancelOrderItemSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Item cancellation validation failed.",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            item = OrderService.cancel_order_item(
                order_id=order_id,
                item_id=item_id,
                reason=serializer.validated_data["reason"]
            )
        except ValidationError as e:
            return Response({
                "success": False,
                "message": e.messages[0],
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "message": "Item cancelled successfully.",
            "data": {
                "item_id": item.id,
                "product_name": item.product.product_name,
                "item_status": item.item_status,
                "cancellation_reason": item.cancellation_reason,
            }
        }, status=status.HTTP_200_OK)
    
class RequestReplacementAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTakeawayStaffOrAdminOrSupervisor]

    def post(self, request, order_id, item_id):
        serializer = ReplacementRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Replacement request validation failed.",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            replacement_request = OrderService.request_replacement(
                order_id=order_id,
                item_id=item_id,
                requested_by=request.user,
                reason=serializer.validated_data["reason"]
            )
        except ValidationError as e:
            return Response({
                "success": False,
                "message": e.messages[0],
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "message": "Replacement request created successfully.",
            "data": {
                "replacement_request_id": replacement_request.id,
                "order_id": replacement_request.order.order_id,
                "item_id": replacement_request.order_item.id,
                "status": replacement_request.status,
                "reason": replacement_request.reason
            }
        }, status=status.HTTP_201_CREATED)
    
class ApproveReplacementAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSupervisorOrAdmin]

    def post(self, request, replacement_request_id):
        serializer = ReplacementDecisionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Replacement approval validation failed.",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            replacement_request = OrderService.approve_replacement(
                replacement_request_id=replacement_request_id,
                supervisor=request.user,
                supervisor_note=serializer.validated_data.get(
                    "supervisor_note",
                    ""
                )
            )
        except ValidationError as e:
            return Response({
                "success": False,
                "message": e.messages[0],
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "message": "Replacement request approved successfully.",
            "data": {
                "replacement_request_id": replacement_request.id,
                "status": replacement_request.status,
                "order_id": replacement_request.order.order_id,
                "item_id": replacement_request.order_item.id,
                "supervisor_note": replacement_request.supervisor_note,
                "decided_at": replacement_request.decided_at,
            }
        }, status=status.HTTP_200_OK)

class RejectReplacementAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSupervisorOrAdmin]

    def post(self, request, replacement_request_id):
        serializer = ReplacementDecisionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Replacement rejection validation failed.",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            replacement_request = OrderService.reject_replacement(
                replacement_request_id=replacement_request_id,
                supervisor=request.user,
                supervisor_note=serializer.validated_data.get(
                    "supervisor_note",
                    ""
                )
            )
        except ValidationError as e:
            return Response({
                "success": False,
                "message": e.messages[0],
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "message": "Replacement request rejected successfully.",
            "data": {
                "replacement_request_id": replacement_request.id,
                "status": replacement_request.status,
                "order_id": replacement_request.order.order_id,
                "item_id": replacement_request.order_item.id,
                "supervisor_note": replacement_request.supervisor_note,
                "decided_at": replacement_request.decided_at,
            }
        }, status=status.HTTP_200_OK) 

class ReplacementRequestListAPIView(APIView):
    permission_classes = [IsAuthenticated,IsSupervisorOrAdmin]

    def get(self, request):
        replacement_requests = (OrderService.get_pending_replacement_requests())
        serializer = ReplacementRequestListSerializer(replacement_requests,many=True)

        return Response({
            "success": True,
            "message": "Pending replacement requests fetched successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK) 

class ReplacementRequestDetailAPIView(APIView):
    permission_classes = [IsAuthenticated,IsSupervisorOrAdmin]

    def get(self, request, replacement_request_id):

        try:
            data = OrderService.get_replacement_request_detail(replacement_request_id)

        except ValidationError as e:
            return Response({
                "success": False,
                "message": e.messages[0],
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)
        current_serializer = ReplacementRequestDetailSerializer(data["current_request"])
        history_serializer = ReplacementRequestHistorySerializer(data["replacement_history"],many=True)

        return Response({
            "success": True,
            "message": "Replacement request details fetched successfully.",
            "data": {
                "current_request": current_serializer.data,
                "available_quantity": data["available_quantity"],
                "replacement_history": history_serializer.data,
            }
        }, status=status.HTTP_200_OK)
    
class VerifyPickupOTPAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTakeawayStaffOrAdminOrSupervisor]

    def post(self, request, order_id):
        serializer = VerifyOTPSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "OTP validation failed.",
                "data": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = OrderService.verify_pickup_otp(
                order_id=order_id,
                otp=serializer.validated_data["otp"],
            )
        except ValidationError as e:
            return Response({
                "success": False,
                "message": e.messages[0],
                "data": None,
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "message": "OTP verified successfully.",
            "data": {
                "order_id": order.order_id,
                "otp_verified_at": order.otp_verified_at,
                "next_step": "Pickup can now be completed."
            }
        }, status=status.HTTP_200_OK) 
    
class CompletePickupAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTakeawayStaffOrAdminOrSupervisor]

    def post(self, request, order_id):
        try:
            order = OrderService.complete_pickup(
                order_id=order_id,
                takeaway_staff=request.user,
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
                "message": "Pickup completed successfully.",
                "data": {
                    "order_id": order.order_id,
                    "order_status": order.order_status,
                    "picked_up_at": order.picked_up_at,
                },
            },
            status=status.HTTP_200_OK,
        )
    
class PaymentSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTakeawayStaffOrAdminOrSupervisor]

    def get(self, request, order_id):
        try:
            order = OrderService.get_payment_summary(order_id)
        except ValidationError as error:
            return Response(
                {
                    "success": False,
                    "message": error.messages[0],
                    "data": None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = PaymentSummarySerializer(order)

        return Response(
            {
                "success": True,
                "message": "Payment summary fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    
class PackingOrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated,IsPackerOrAdminOrSupervisor,]

    def get(self, request, order_id):
        try:
            order = OrderService.get_packing_order(order_id)

        except ValidationError as e:
            return Response(
                {
                    "success": False,
                    "message": e.messages[0],
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = OrderDetailSerializer(order)

        return Response(
            {
                "success": True,
                "message": "Packing order fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )   

class PickupStatusAPIView(APIView):
    permission_classes = [IsAuthenticated,IsTakeawayStaffOrAdminOrSupervisor]

    def get(self, request, order_id):
        try:
            order = OrderService.get_pickup_status(order_id)
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
                "message": "Pickup status fetched successfully.",
                "data": {
                    "order_id": order.order_id,
                    "order_status": order.order_status,
                    "payment_status": order.payment_status,
                    "pickup_verified": order.pickup_verified,
                    "otp_verified_at": order.otp_verified_at,
                    "pickup_verified_expires_at": (
                        order.pickup_verified_expires_at
                    ),
                },
            },
            status=status.HTTP_200_OK,
        )

    