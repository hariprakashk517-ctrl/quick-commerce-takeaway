from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import ProductService
from .serializers import *
from .models import *
from accounts.permissions import *



class ProductListCreateAPIView(APIView):

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsAdminOrSupervisor()]
        
        return [IsAuthenticated()]

    def get(self, request):
        if request.user.role == "CUSTOMER":
            products = ProductService.list_products_for_customer_store(
                request.user
            )
            serializer = CustomerProductSerializer(products, many=True)

        else:
            products = ProductService.list_active_products()
            serializer = ProductSerializer(products, many=True)

        return Response(
            {
                "success": True,
                "message": "Products fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = ProductService.create_product(serializer.validated_data)
            response_serializer = ProductSerializer(product)
            return Response(
                {
                    "success": True,
                    "message": "Product created successfully.",
                    "data": response_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "success": False,
                "message": "Product creation failed.",
                "data": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
class ProductDetailAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["PATCH","DELETE"]:
            return [IsAuthenticated(), IsAdminOrSupervisor()]

        return [IsAuthenticated()]

    def get_object(self, pk):
        return ProductService.get_product(pk)

    def get(self, request, pk):
        inventory = ProductService.get_product_for_customer_store(customer=request.user,product_id=pk,)

        if inventory is None:
            return Response({
                    "success": False,
                    "message": "Product not found.",
                    "data": None
                },status=status.HTTP_404_NOT_FOUND
            )

        serializer = CustomerProductSerializer(inventory)

        return Response({
                "success": True,
                "message": "Product fetched successfully.",
                "data": serializer.data
            },status=status.HTTP_200_OK
        )

    def patch(self, request, pk):
        product = self.get_object(pk)

        if product is None:
            return Response({
                    "success": False,
                    "message": "Product not found.",
                    "data": None
                },status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(product,data=request.data,partial=True)

        if serializer.is_valid():

            updated_product = ProductService.update_product(product,serializer.validated_data)
            response_serializer = ProductSerializer(updated_product)

            return Response({
                    "success": True,
                    "message": "Product updated successfully.",
                    "data": response_serializer.data
                },status=status.HTTP_200_OK
            )
        
        return Response({
                "success": False,
                "message": "Product update failed.",
                "data": serializer.errors
            },status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        product = self.get_object(pk)

        if product is None:
            return Response({
                    "success": False,
                    "message": "Product not found.",
                    "data": None
                },status=status.HTTP_404_NOT_FOUND
            )

        ProductService.deactivate_product(product)
        # product.is_active = False
        # product.save(update_fields=["is_active", "updated_at"])

        return Response({
                "success": True,
                "message": "Product deactivated successfully.",
                "data": None
            },status=status.HTTP_200_OK
        )
    
