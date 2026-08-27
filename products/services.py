from rest_framework.exceptions import NotFound
from .models import Product
from inventory.models import Inventory
from stores.services import StoreService


class ProductService:

    @staticmethod
    def create_product(validated_data):
        return Product.objects.create(**validated_data)

    @staticmethod
    def list_active_products():
        return Product.objects.filter(is_active=True)

    @staticmethod
    def get_product(product_id):
        try:
            return Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return None

    @staticmethod
    def update_product(product, validated_data):
        for field, value in validated_data.items():
            setattr(product, field, value)

        product.save()
        return product

    @staticmethod
    def deactivate_product(product):
        product.is_active = False
        product.save(update_fields=["is_active", "updated_at"])
        return product
    
    @staticmethod
    def list_products_for_customer_store(customer):
        store_context = StoreService.get_customer_active_context(customer)
        store = store_context["store"]

        inventory_qs = Inventory.objects.select_related(
            "product",
            "store"
        ).filter(
            store=store,
            product__is_active=True,
            # available_quantity__gt=0
        )

        return inventory_qs

    @staticmethod
    def get_product_for_customer_store(customer, product_id):
        store_context = StoreService.get_customer_active_context(customer)
        store = store_context["store"]

        inventory = Inventory.objects.select_related(
            "product",
            "store"
        ).filter(
            store=store,
            product_id=product_id,
            product__is_active=True,
        ).first()

        if not inventory:
            raise NotFound("Product is not available in your selected store.")

        return inventory