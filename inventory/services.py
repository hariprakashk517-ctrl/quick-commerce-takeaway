from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Inventory


class InventoryService:
    @staticmethod
    @transaction.atomic
    def reserve_stock(store, product, quantity):
        inventory = Inventory.objects.select_for_update().get(
            store=store,
            product=product
        )
        if inventory.available_quantity < quantity:
            raise ValidationError("Insufficient stock available.")

        inventory.available_quantity -= quantity
        inventory.reserved_quantity += quantity
        inventory.save(update_fields=[
            "available_quantity",
            "reserved_quantity",
            "updated_at"
        ])
        return inventory
    
    @staticmethod
    @transaction.atomic
    def restore_stock(store, product, quantity):
        inventory = Inventory.objects.select_for_update().get(
            store=store,
            product=product)
        
        if inventory is None:
            raise ValidationError("Product is not available in the selected store.")
        
        if inventory.reserved_quantity < quantity:
            raise ValidationError("Reserved stock is less than restore quantity.")
        
        inventory.reserved_quantity -= quantity
        inventory.available_quantity += quantity
        inventory.save(update_fields=[
            "available_quantity",
            "reserved_quantity",
            "updated_at"
        ])
        return inventory
    
    @staticmethod
    @transaction.atomic
    def mark_stock_sold(store, product, quantity):
        inventory = Inventory.objects.select_for_update().get(
            store=store,
            product=product
        )
        if inventory.reserved_quantity < quantity:
            raise ValidationError("Reserved stock is less than sold quantity.")
        inventory.reserved_quantity -= quantity
        inventory.save(update_fields=[
            "reserved_quantity",
            "updated_at"
        ])
        return inventory
    
    @staticmethod
    def create_inventory(validated_data):
        return Inventory.objects.create(**validated_data)


    @staticmethod
    def list_inventory(store=None):
        queryset = Inventory.objects.select_related("store","product")

        if store is not None:
            queryset = queryset.filter(store=store)

        return queryset


    @staticmethod
    def get_inventory(inventory_id, store=None):
        queryset = Inventory.objects.select_related("store","product")

        if store is not None:
            queryset = queryset.filter(store=store)

        try:
            return queryset.get(pk=inventory_id)
        except Inventory.DoesNotExist:
            return None


    @staticmethod
    def update_inventory(inventory, validated_data):
        for field, value in validated_data.items():
            setattr(inventory, field, value)

        inventory.save()
        return inventory