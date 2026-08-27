from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    
    selected_store_name = serializers.CharField(source="selected_store.store_name",read_only=True)
    
    class Meta:
        model = Address
        fields = [
            "id",
            "address_type",
            "full_address",
            "latitude",
            "longitude",
            "is_default",
            "last_used",
            "created_at",
            "updated_at",
            "selected_store",
            "distance_from_store_km",
            "selected_store_name",
        ]
        read_only_fields = ["id", "created_at", "selected_store_name", "distance_from_store_km", "updated_at"]