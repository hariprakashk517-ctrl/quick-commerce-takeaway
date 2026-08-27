from .models import Address
from django.db import transaction
from stores.services import StoreService
from rest_framework.exceptions import ValidationError

class AddressService:

    @staticmethod
    @transaction.atomic
    def create_address(customer, validated_data):
        if validated_data.get("is_default"):
            Address.objects.filter(customer=customer).update(is_default=False)

        if validated_data.get("last_used"):
            Address.objects.filter(customer=customer).update(last_used=False)

        store, distance_km = StoreService.find_nearest_store(
        validated_data["latitude"],
        validated_data["longitude"]
        )

        validated_data["selected_store"] = store
        validated_data["distance_from_store_km"] = distance_km

        return Address.objects.create(customer=customer,**validated_data)

    @staticmethod
    def list_addresses(customer):
        return Address.objects.filter(customer=customer)

    @staticmethod
    def get_address(customer, address_id):
        try:
            return Address.objects.get(
                id=address_id,
                customer=customer
            )
        except Address.DoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def update_address(address, validated_data):
        customer = address.customer

        if validated_data.get("is_default"):
            Address.objects.filter(customer=customer).exclude(id=address.id).update(is_default=False)

        if validated_data.get("last_used"):
            Address.objects.filter(customer=customer).exclude(id=address.id).update(last_used=False)

        for field, value in validated_data.items():
            setattr(address, field, value)

        if "latitude" in validated_data or "longitude" in validated_data:
            latitude = validated_data.get("latitude", address.latitude)
            longitude = validated_data.get("longitude", address.longitude)

            store, distance_km = StoreService.find_nearest_store(latitude,longitude)

            address.selected_store = store
            address.distance_from_store_km = distance_km

        address.save()
        return address

    @staticmethod
    def delete_address(address):
        address.delete()
        return True

    # @staticmethod
    # def get_active_address(customer):
    #     address = (Address.objects.select_related("selected_store").filter(customer=customer,last_used=True,).first())

    #     if not address:
    #         address = (Address.objects.select_related("selected_store").filter(customer=customer,is_default=True,).first())

    #     if not address:
    #         raise ValidationError({"address": "Please select a delivery address."})

    #     if not address.selected_store:
    #         raise ValidationError({"store": ("No store is assigned to the selected address.")})

    #     if not address.selected_store.is_active:
    #         raise ValidationError({"store": ("The store assigned to this address is currently inactive.")})

    #     return address

    @staticmethod
    def get_default_address(customer):

        address = (
            Address.objects
            .select_related("selected_store")
            .filter(
                customer=customer,
                is_default=True,
            )
            .first()
        )

        return address