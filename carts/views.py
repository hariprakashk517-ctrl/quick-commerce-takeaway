from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .services import CartService
from .serializers import CartSerializer
from django.core.exceptions import ValidationError


class CartDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cart = CartService.get_cart(request.user)
        except ValidationError as e:
            return Response(
                {
                    "success": False,
                    "message": e.messages[0],
                    "data": None
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CartSerializer(cart)

        return Response({
            "success": True,
            "message": "Cart fetched successfully.",
            "data": serializer.data
        },status=status.HTTP_200_OK)

class AddCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        try:
            cart_item = CartService.add_item_to_cart(
                customer=request.user,
                product_id=product_id,
                quantity=int(quantity)
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
            "message": "Item added to cart successfully.",
            "data": {"cart_item_id": cart_item.id}
        },status=status.HTTP_201_CREATED)

class UpdateCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        try:
            cart_item = CartService.update_cart_item(
                customer=request.user,
                product_id=product_id,
                quantity=int(quantity)
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
            "message": "Cart item updated successfully.",
            "data": {
                "cart_item_id": cart_item.id,
                "quantity": cart_item.quantity
            }
        },status=status.HTTP_200_OK)

class RemoveCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        product_id = request.data.get("product_id")

        try:
            CartService.remove_cart_item(
                customer=request.user,
                product_id=product_id
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

        return Response(
            {
                "success": True,
                "message": "Item removed from cart successfully.",
                "data": None
            },status=status.HTTP_200_OK
        )
    
class ClearCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            CartService.clear_cart(request.user)
        except ValidationError as e:
            return Response(
                {
                    "success": False,
                    "message": e.messages[0],
                    "data": None
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message": "Cart cleared successfully.",
                "data": None
            },status=status.HTTP_200_OK
        )