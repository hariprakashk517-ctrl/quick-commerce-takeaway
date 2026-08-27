from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import *
from .serializers import InventorySerializer
from .services import InventoryService

class InventoryListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSupervisor]

    def get(self, request):

        if request.user.role == "ADMIN":
            inventory = InventoryService.list_inventory()

        else:
            if request.user.store is None:
                return Response({
                        "success": False,
                        "message": "User is not assigned to a store.",
                        "data": None
                    },status=status.HTTP_400_BAD_REQUEST
                )

            inventory = InventoryService.list_inventory(store=request.user.store)

        serializer = InventorySerializer(inventory,many=True)

        return Response({
                "success": True,
                "message": "Inventory fetched successfully.",
                "data": serializer.data
            },status=status.HTTP_200_OK
        )

    def post(self, request):

        serializer = InventorySerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                    "success": False,
                    "message": "Inventory creation failed.",
                    "data": serializer.errors
                },status=status.HTTP_400_BAD_REQUEST
            )

        requested_store = serializer.validated_data["store"]

        if request.user.role == "SUPERVISOR":

            if request.user.store is None:
                return Response({
                        "success": False,
                        "message": "User is not assigned to a store.",
                        "data": None
                    },status=status.HTTP_400_BAD_REQUEST
                )

            if requested_store.id != request.user.store.id:
                return Response({
                        "success": False,
                        "message": "You can only manage inventory for your assigned store.",
                        "data": None
                    },status=status.HTTP_403_FORBIDDEN
                )
            
        inventory = InventoryService.create_inventory(serializer.validated_data)
        response_serializer = InventorySerializer(inventory)

        return Response({
                "success": True,
                "message": "Inventory created successfully.",
                "data": response_serializer.data
            },status=status.HTTP_201_CREATED
        )
    
class InventoryDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSupervisor]

    def get_object(self, request, pk):

        # ADMIN can access any store
        if request.user.role == "ADMIN":
            return InventoryService.get_inventory(pk)

        # SUPERVISOR must have a store
        if request.user.store is None:
            return None

        # SUPERVISOR can access only own store
        return InventoryService.get_inventory(pk,store=request.user.store)

    def get(self, request, pk):

        inventory = self.get_object(request, pk)

        if inventory is None:
            return Response({
                    "success": False,
                    "message": "Inventory not found.",
                    "data": None
                },status=status.HTTP_404_NOT_FOUND
            )

        serializer = InventorySerializer(inventory)

        return Response({
                "success": True,
                "message": "Inventory fetched successfully.",
                "data": serializer.data
            },status=status.HTTP_200_OK
        )

    def patch(self, request, pk):

        inventory = self.get_object(request, pk)

        if inventory is None:
            return Response({
                    "success": False,
                    "message": "Inventory not found.",
                    "data": None
                },status=status.HTTP_404_NOT_FOUND
            )

        serializer = InventorySerializer(inventory,data=request.data,partial=True)

        if serializer.is_valid():

            # Supervisor cannot change inventory to another store
            if request.user.role == "SUPERVISOR":

                requested_store = serializer.validated_data.get("store",inventory.store)

                if requested_store.id != request.user.store.id:
                    return Response({
                            "success": False,
                            "message": "You can only manage inventory for your assigned store.",
                            "data": None
                        },status=status.HTTP_403_FORBIDDEN
                    )

            inventory = InventoryService.update_inventory(inventory,serializer.validated_data)
            response_serializer = InventorySerializer(inventory)

            return Response({
                    "success": True,
                    "message": "Inventory updated successfully.",
                    "data": response_serializer.data
                },status=status.HTTP_200_OK
            )

        return Response({
                "success": False,
                "message": "Inventory update failed.",
                "data": serializer.errors
            },status=status.HTTP_400_BAD_REQUEST
        )