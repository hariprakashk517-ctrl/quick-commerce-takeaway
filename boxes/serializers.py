from rest_framework import serializers
from orders.models import Order

class AssignBoxSerializer(serializers.Serializer):
    order_id = serializers.CharField()
    box_id = serializers.CharField()

class BoxOrderSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source="store.store_name",read_only=True)
    box_id = serializers.CharField(source="box.box_id",read_only=True)
    class Meta:
        model = Order
        fields = [
            "id",
            "order_id",
            "box_id",
            "store_name",
            "fulfillment_mode",
            "order_status",
            "created_at",
        ]