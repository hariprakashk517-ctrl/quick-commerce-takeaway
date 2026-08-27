from rest_framework import serializers
from .models import *


class CreateOrderSerializer(serializers.Serializer):
    fulfillment_mode = serializers.ChoiceField(
        choices=[
            ("DELIVERY", "Delivery"),
            ("TAKEAWAY", "Takeaway"),
        ],
        default="DELIVERY"
    )

    payment_type = serializers.ChoiceField(
        choices=[
            ("PREPAID", "Prepaid"),
            ("PAY_AT_TAKEAWAY", "Pay at Takeaway"),
        ]
    )

class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "order_id",
            "order_status",
            "fulfillment_mode",
            "payment_status",
            "refund_status",
            "total_amount",
            "created_at",
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.product_name",
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "unit_price",
            "total_price",
            "item_status",
            "is_verified",
        ]

class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    store_name = serializers.CharField(
        source="store.store_name",
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "order_id",
            "customer",
            "store",
            "store_name",
            "fulfillment_mode",
            "order_status",
            "payment_status",
            "refund_status",
            "total_amount",
            "items",
            "created_at",
            "updated_at",
        ]

class VerificationItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.product_name",
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "item_status",
            "is_verified",
        ]

class OrderItemVerificationSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source="product.id", read_only=True)
    product_name = serializers.CharField(source="product.product_name", read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product_id",
            "product_name",
            "quantity",
            "item_status",
            "is_verified",
        ]

class OrderVerificationSerializer(serializers.ModelSerializer):
    box_id = serializers.CharField(source="box.box_id", read_only=True)
    items = OrderItemVerificationSerializer(many=True, read_only=True)
    next_step = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "order_id",
            "order_status",
            "box_id",
            "items",
            "next_step",
        ]

    def get_next_step(self, obj):
        return "VERIFY_OR_RESOLVE_ITEMS"
    
class CancelOrderItemSerializer(serializers.Serializer):
    reason = serializers.ChoiceField(
        choices=[
            ("WRONG_ITEM", "Wrong Item Packed"),
            ("DAMAGED_ITEM", "Damaged Item"),
            ("ITEM_MISSING", "Item Missing"),
            ("CUSTOMER_DECLINED", "Customer Declined Item"),
            ("QUALITY_ISSUE", "Quality Issue"),
            ("OTHER", "Other"),
        ]
    )

class ReplacementRequestSerializer(serializers.Serializer):
    reason = serializers.ChoiceField(choices=ReplacementRequest.REPLACEMENT_REASON_CHOICES)
    # replacement_product_id = serializers.IntegerField(required=False,allow_null=True)
    
class ReplacementDecisionSerializer(serializers.Serializer):
    supervisor_note = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500
    )

class ReplacementRequestListSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(source="order.order_id",read_only=True)
    item_id = serializers.IntegerField(source="order_item.id",read_only=True)
    product_name = serializers.CharField(source="order_item.product.product_name",read_only=True)
    quantity = serializers.IntegerField(source="order_item.quantity",read_only=True)

    class Meta:
        model = ReplacementRequest
        fields = [
            "id",
            "order_id",
            "item_id",
            "product_name",
            "quantity",
            "reason",
            "status",
            "created_at",
        ]

class ReplacementRequestDetailSerializer(serializers.ModelSerializer):

    order_id = serializers.CharField(source="order.order_id",read_only=True)
    item_id = serializers.IntegerField(source="order_item.id",read_only=True)
    product_id = serializers.IntegerField(source="order_item.product.id",read_only=True)
    product_name = serializers.CharField(source="order_item.product.product_name",read_only=True)
    quantity = serializers.IntegerField(source="order_item.quantity",read_only=True)
    reason_display = serializers.CharField(source="get_reason_display",read_only=True)
    status_display = serializers.CharField(source="get_status_display",read_only=True)

    class Meta:
        model = ReplacementRequest
        fields = [
            "id",
            "order_id",
            "item_id",
            "product_id",
            "product_name",
            "quantity",
            "reason",
            "reason_display",
            "status",
            "status_display",
            "supervisor_note",
            "created_at",
            "decided_at",
        ]

class ReplacementRequestHistorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="order_item.product.product_name",read_only=True)
    reason_display = serializers.CharField(source="get_reason_display",read_only=True)
    status_display = serializers.CharField(source="get_status_display",read_only=True)

    class Meta:
        model = ReplacementRequest
        fields = [
            "id",
            "product_name",
            "reason",
            "reason_display",
            "status",
            "status_display",
            "supervisor_note",
            "created_at",
            "decided_at",
        ]

class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(
        min_length=4,
        max_length=4
    )

class PaymentSummarySerializer(serializers.ModelSerializer):
    selected_payment_type = serializers.CharField(source="payment_type",read_only=True)
    collected_payment_type = serializers.CharField(source="payment.payment_type",read_only=True,allow_null=True)
    next_step = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "order_id",
            "total_amount",
            "payment_status",
            "selected_payment_type",
            "collected_payment_type",
            "verification_completed",
            "next_step",
        ]

    def get_next_step(self, obj):
        if obj.payment_status == "PAID":
            return "VERIFY_OTP"

        if obj.payment_type == "PAY_AT_TAKEAWAY":
            return "COLLECT_PAYMENT"

        return "COLLECT_PAYMENT"