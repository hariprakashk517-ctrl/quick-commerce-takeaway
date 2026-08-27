from rest_framework import serializers

class CheckoutSerializer(serializers.Serializer):
    fulfillment_mode = serializers.ChoiceField(
        choices=[
            ("DELIVERY", "Delivery"),
            ("TAKEAWAY", "Takeaway"),
        ]
    )

    payment_type = serializers.ChoiceField(
        choices=[
            ("PREPAID", "Prepaid"),
            ("CASH_ON_PICKUP", "Cash on Pickup"),
            ("UPI_ON_PICKUP", "UPI on Pickup"),
            ("CARD_ON_PICKUP", "Card on Pickup"),
        ]
    )