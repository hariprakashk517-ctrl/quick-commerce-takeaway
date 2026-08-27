from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdminOrSupervisor
from .serializers import *
from .services import *

class StoreListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSupervisor]

    def get(self, request):
        stores = StoreService.list_stores()
        serializer = StoreSerializer(stores, many=True)

        return Response({
            "success": True,
            "message": "Stores fetched successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = StoreSerializer(data=request.data)

        if serializer.is_valid():
            store = StoreService.create_store(serializer.validated_data)
            response_serializer = StoreSerializer(store)

            return Response({
                "success": True,
                "message": "Store created successfully.",
                "data": response_serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "message": "Store creation failed.",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
class StoreDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSupervisor]

    def get_object(self, pk):
        return StoreService.get_store(pk)

    def get(self, request, pk):
        store = self.get_object(pk)

        if store is None:
            return Response({
                "success": False,
                "message": "Store not found.",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = StoreSerializer(store)

        return Response({
            "success": True,
            "message": "Store fetched successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        store = self.get_object(pk)

        if store is None:
            return Response({
                "success": False,
                "message": "Store not found.",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = StoreSerializer(store, data=request.data, partial=True)

        if serializer.is_valid():
            updated_store = StoreService.update_store(store,serializer.validated_data)
            response_serializer = StoreSerializer(updated_store)

            return Response({
                "success": True,
                "message": "Store updated successfully.",
                "data": response_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "message": "Store update failed.",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        store = self.get_object(pk)

        if store is None:
            return Response({
                "success": False,
                "message": "Store not found.",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            StoreService.delete_store(store)
        except ValidationError as e:
            return Response({
                "success": False,
                "message": e.messages[0],
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "message": "Store deleted successfully.",
            "data": None
        }, status=status.HTTP_200_OK)