from rest_framework import serializers
from .models import Cart, CartItem
from decimal import Decimal


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.product_name", read_only=True)
    price = serializers.DecimalField(source="product.price", max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.SerializerMethodField()
    product_id = serializers.IntegerField(source="product.id",read_only=True)

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product_id",
            "product_name",
            "price",
            "quantity",
            "total_price",
        ]

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    cart_total = serializers.SerializerMethodField()
    store_id = serializers.IntegerField(source="store.id",read_only=True)
    store_name = serializers.CharField(source="store.store_name",read_only=True)

    class Meta:
        model = Cart
        fields = [
            "id",
            "customer",
            "store_id",
            "store_name",
            "items",
            "cart_total",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["customer"]

    def get_cart_total(self, obj):
        return sum((item.product.price * item.quantity for item in obj.items.all()),Decimal("0.00"))