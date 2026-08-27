from django.core.exceptions import ValidationError
from products.models import Product
from .models import Cart, CartItem
from stores.services import *
from inventory.models import Inventory


class CartService:
    @staticmethod
    def add_item_to_cart(customer, product_id, quantity):
        if quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")

        cart = CartService.get_cart(customer)

        inventory = Inventory.objects.filter(
            store=cart.store,
            product_id=product_id,
            product__is_active=True
        ).select_related("product").first()

        if inventory is None:
            raise ValidationError("Product is not available in your selected store.")

        if inventory.available_quantity < 1:
            raise ValidationError("Product is currently out of stock.")

        existing_cart_item = CartItem.objects.filter(
            cart=cart,
            product=inventory.product
        ).first()

        existing_quantity = existing_cart_item.quantity if existing_cart_item else 0
        final_quantity = existing_quantity + quantity

        if final_quantity > inventory.available_quantity:
            raise ValidationError("Requested quantity exceeds available stock.")

        if existing_cart_item:
            existing_cart_item.quantity = final_quantity
            existing_cart_item.save(update_fields=["quantity", "updated_at"])
            return existing_cart_item

        return CartItem.objects.create(
            cart=cart,
            product=inventory.product,
            quantity=quantity
        )

    @staticmethod
    def update_cart_item(customer, product_id, quantity):
        if quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")

        cart = CartService.get_cart(customer)

        inventory = Inventory.objects.filter(
            store=cart.store,
            product_id=product_id,
            product__is_active=True
        ).select_related("product").first()

        if inventory is None:
            raise ValidationError("Product is not available in your selected store.")

        if inventory.available_quantity < 1:
            raise ValidationError("Product is currently out of stock.")

        if quantity > inventory.available_quantity:
            raise ValidationError("Requested quantity exceeds available stock.")

        cart_item = CartItem.objects.get(
            cart=cart,
            product=inventory.product
        )

        cart_item.quantity = quantity
        cart_item.save(update_fields=["quantity", "updated_at"])

        return cart_item
    
    @staticmethod
    def remove_cart_item(customer, product_id):
        cart = Cart.objects.get(customer=customer)
        cart_item = CartItem.objects.get(
            cart=cart,
            product_id=product_id
        )
        cart_item.delete()
        return True
    
    @staticmethod
    def get_cart(customer):
        store_context = StoreService.get_customer_active_context(customer)
        store = store_context["store"]

        cart, created = Cart.objects.get_or_create(
            customer=customer,
            defaults={"store": store})

        if cart.store != store:
            cart.items.all().delete()
            cart.store = store
            cart.save(update_fields=["store", "updated_at"])

        cart.items.all().order_by("id")

        return cart
    
    @staticmethod
    def clear_cart(customer):
        cart = Cart.objects.get(customer=customer)
        cart.items.all().delete()
        return True
