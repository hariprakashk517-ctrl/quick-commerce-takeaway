from django.core.exceptions import ValidationError
from django.db import transaction
from carts.services import CartService
from inventory.models import Inventory


class CheckoutService:

    @staticmethod
    @transaction.atomic
    def checkout(customer, fulfillment_mode, payment_type):
        cart = CartService.get_cart(customer)

        if not cart.items.exists():
            raise ValidationError("Cart is empty.")

        for cart_item in cart.items.select_related("product"):
            inventory = Inventory.objects.select_for_update().filter(
                store=cart.store,
                product=cart_item.product,
                product__is_active=True
            ).first()

            if inventory is None:
                raise ValidationError(
                    f"{cart_item.product.product_name} is not available in your selected store."
                )

            if inventory.available_quantity < 1:
                raise ValidationError(
                    f"{cart_item.product.product_name} is currently out of stock."
                )

            if cart_item.quantity > inventory.available_quantity:
                raise ValidationError(
                    f"Only {inventory.available_quantity} units available for {cart_item.product.product_name}."
                )
            
        items = []
        cart_total = 0

        for cart_item in cart.items.select_related("product"):
            item_total = cart_item.product.price * cart_item.quantity

            items.append({
                "product_id": cart_item.product.id,
                "product_name": cart_item.product.product_name,
                "quantity": cart_item.quantity,
                "unit_price": cart_item.product.price,
                "total_price": item_total,
            })

            cart_total += item_total

        return {
            "cart": cart,
            "store": cart.store,
            "fulfillment_mode": fulfillment_mode,
            "payment_type": payment_type,
            "items": items,
            "cart_total": cart_total,
            }
    
    