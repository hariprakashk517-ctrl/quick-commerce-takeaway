import math
from django.core.exceptions import ValidationError
from .models import *
from addresses.models import *


class StoreService:

    @staticmethod
    def calculate_distance_km(lat1, lon1, lat2, lon2):
        radius = 6371

        lat1 = math.radians(float(lat1))
        lon1 = math.radians(float(lon1))
        lat2 = math.radians(float(lat2))
        lon2 = math.radians(float(lon2))

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return radius * c
    
    @staticmethod
    def find_nearest_store(latitude, longitude):
        active_stores = Store.objects.filter(is_active=True)

        if not active_stores.exists():
            raise ValidationError("No active store available.")

        nearest_store = None
        nearest_distance = None

        for store in active_stores:
            distance = StoreService.calculate_distance_km(latitude, longitude, store.latitude, store.longitude)

            if nearest_distance is None or distance < nearest_distance:
                nearest_store = store
                nearest_distance = distance

        return nearest_store, round(nearest_distance, 2)
    
    @staticmethod
    def ensure_active_store(address):
        if (address.selected_store is None or not address.selected_store.is_active):
            store, distance_km = StoreService.find_nearest_store(address.latitude,address.longitude)

            address.selected_store = store
            address.distance_from_store_km = distance_km
            address.save(update_fields=[
                "selected_store",
                "distance_from_store_km",
                "updated_at"])
        return address.selected_store, address.distance_from_store_km

    @staticmethod
    def get_customer_active_context(customer):
        address = Address.objects.filter(
            customer=customer,
            last_used=True
        ).first()

        if address is None:
            address = Address.objects.filter(
                customer=customer,
                is_default=True
            ).first()

        if address is None:
            raise ValidationError("Customer address is required.")

        store, distance_km = StoreService.ensure_active_store(address)

        return {
            "address": address,
            "store": store,
            "distance_km": distance_km
        }
    
    @staticmethod
    def create_store(validated_data):
        return Store.objects.create(**validated_data)

    @staticmethod
    def list_stores():
        return Store.objects.all().order_by("store_name")

    @staticmethod
    def get_store(store_id):
        try:
            return Store.objects.get(id=store_id)
        except Store.DoesNotExist:
            return None

    @staticmethod
    def update_store(store, validated_data):
        for field, value in validated_data.items():
            setattr(store, field, value)

        store.save()
        return store

    @staticmethod
    def delete_store(store):
        if store.inventories.exists():
            raise ValidationError("Cannot delete store because inventory exists.")

        store.delete()
        return True