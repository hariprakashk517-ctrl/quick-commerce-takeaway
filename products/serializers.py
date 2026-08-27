from rest_framework import serializers
from .models import Product
from inventory.models import Inventory


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "sku",
            "product_name",
            "description",
            "price",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

class CustomerProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source="product.id", read_only=True)
    sku = serializers.CharField(source="product.sku", read_only=True)
    product_name = serializers.CharField(source="product.product_name", read_only=True)
    description = serializers.CharField(source="product.description", read_only=True)
    price = serializers.DecimalField(source="product.price", max_digits=10, decimal_places=2, read_only=True)
    store_id = serializers.IntegerField(source="store.id", read_only=True)
    store_name = serializers.CharField(source="store.store_name", read_only=True)
    # available_quantity = serializers.IntegerField()
    stock_status = serializers.SerializerMethodField()
    in_stock = serializers.SerializerMethodField()
    can_add_to_cart = serializers.SerializerMethodField()

    class Meta:
        model = Inventory
        fields = [
            "product_id",
            "sku",
            "product_name",
            "description",
            "price",
            "store_id",
            "store_name",
            # "available_quantity",
            "stock_status",
            "in_stock",
            "can_add_to_cart",
        ]

    # def get_in_stock(self, obj):
    #     return obj.available_quantity > 0

    # def get_stock_status(self, obj):
    #     return "IN_STOCK" if obj.available_quantity > 0 else "OUT_OF_STOCK"
    
    # def get_can_add_to_cart(self, obj):
    #     return obj.available_quantity > 0

    def get_in_stock(self, obj):
        return (
            obj.available_quantity > 0
            and obj.product.is_active
            and obj.store.is_active
        )

    def get_stock_status(self, obj):
        return "IN_STOCK" if self.get_in_stock(obj) else "OUT_OF_STOCK"

    def get_can_add_to_cart(self, obj):
        return self.get_in_stock(obj)