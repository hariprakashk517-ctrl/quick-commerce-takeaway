from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsTakeawayStaffOrAdminOrSupervisor
from .serializers import *
from .services import BoxService


class AssignBoxAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTakeawayStaffOrAdminOrSupervisor]

    def post(self, request):
        serializer = AssignBoxSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Box assignment validation failed.",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            box = BoxService.assign_box(
                order_id=serializer.validated_data["order_id"],
                box_id=serializer.validated_data["box_id"]
            )
        except ValidationError as e:
            return Response({
                "success": False,
                "message": e.messages[0],
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "message": "Box assigned successfully.",
            "data": {
                "box_id": box.box_id,
                "order_id": box.assigned_order.order_id,
                "status": box.status
            }
        }, status=status.HTTP_200_OK)

class PackingDoneOrdersAPIView(APIView):
    permission_classes = [IsAuthenticated,IsTakeawayStaffOrAdminOrSupervisor]

    def get(self,request):
        order =BoxService.get_packing_done_orders()

        serializer = BoxOrderSerializer(order, many=True)

        return Response({
            "success": True,
            "message": "Packing done orders fetched successfully.",
            "data": serializer.data,
        }, status=status.HTTP_200_OK)

class BoxAssignedOrdersAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsTakeawayStaffOrAdminOrSupervisor,
    ]

    def get(self, request):
        orders = BoxService.get_box_assigned_orders()

        serializer = BoxOrderSerializer(orders,many=True)

        return Response({
            "success": True,
            "message": "Box assigned orders fetched successfully.",
            "data": serializer.data,
        }, status=status.HTTP_200_OK)