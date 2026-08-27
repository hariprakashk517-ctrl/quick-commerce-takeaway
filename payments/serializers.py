from rest_framework import serializers


class CollectPaymentSerializer(serializers.Serializer):
    payment_type = serializers.ChoiceField(
        choices=[
            ("CASH_ON_PICKUP", "Cash on Pickup"),
            ("UPI_ON_PICKUP", "UPI on Pickup"),
            ("CARD_ON_PICKUP", "Card on Pickup"),
        ]
    )

    transaction_id = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=100
    )

    def validate(self, attrs):
        payment_type = attrs["payment_type"]
        transaction_id = attrs.get("transaction_id", "").strip()

        if payment_type in ["UPI_ON_PICKUP", "CARD_ON_PICKUP"] and not transaction_id:
            raise serializers.ValidationError({"transaction_id": "Transaction ID is required for UPI and card payments."})

        return attrs
    
class CashHandoverSerializer(serializers.Serializer):
    supervisor_note = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500
    )