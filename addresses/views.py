from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsCustomer
from .serializers import AddressSerializer
from .services import AddressService


class AddressListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request):
        addresses = AddressService.list_addresses(request.user)
        serializer = AddressSerializer(addresses, many=True)

        return Response({
            "success": True,
            "message": "Addresses fetched successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)

        if serializer.is_valid():
            address = AddressService.create_address(request.user,serializer.validated_data)
            response_serializer = AddressSerializer(address)
            return Response({
                "success": True,
                "message": "Address created successfully.",
                "data": response_serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "message": "Address creation failed.",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
class AddressDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_object(self, request, pk):
        return AddressService.get_address(request.user, pk)

    def get(self, request, pk):
        address = self.get_object(request, pk)

        if address is None:
            return Response({
                "success": False,
                "message": "Address not found.",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = AddressSerializer(address)

        return Response({
            "success": True,
            "message": "Address fetched successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        address = self.get_object(request, pk)

        if address is None:
            return Response({
                "success": False,
                "message": "Address not found.",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = AddressSerializer(address, data=request.data, partial=True)

        if serializer.is_valid():
            updated_address = AddressService.update_address(address,serializer.validated_data)
            response_serializer = AddressSerializer(updated_address)
            return Response({
                "success": True,
                "message": "Address updated successfully.",
                "data": response_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "message": "Address update failed.",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        address = self.get_object(request, pk)

        if address is None:
            return Response({
                "success": False,
                "message": "Address not found.",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

        AddressService.delete_address(address)

        return Response({
            "success": True,
            "message": "Address deleted successfully.",
            "data": None
        }, status=status.HTTP_200_OK)

class DefaultAddressAPIView(APIView):

    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request):

        address = AddressService.get_default_address(request.user)
        if not address:
            return Response({
                "success": False,
                "message": "No default address found.",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

        response_serializer = AddressSerializer(address)

        return Response({
            "success": True,
            "message": "Default address retrieved successfully.",
            "data": response_serializer.data
        }, status=status.HTTP_200_OK)