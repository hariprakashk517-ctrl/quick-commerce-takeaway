from rest_framework import serializers
from .models import *


class InventorySerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source="store.store_name", read_only=True)
    product_name = serializers.CharField(source="product.product_name", read_only=True)

    class Meta:
        model = Inventory
        fields = [
            "id",
            "store",
            "store_name",
            "product",
            "product_name",
            "available_quantity",
            "reserved_quantity",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]