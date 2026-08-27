from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from orders.models import Order
from .models import Box


class BoxService:

    @staticmethod
    @transaction.atomic
    def assign_box(order_id, box_id):
        order = Order.objects.select_for_update().filter(
            order_id=order_id
        ).first()

        if order is None:
            raise ValidationError("Order not found.")

        if order.fulfillment_mode != "TAKEAWAY":
            raise ValidationError("Box assignment is only allowed for takeaway orders.")

        if order.order_status != "PACKING_DONE":
            raise ValidationError("Only PACKING_DONE orders can be assigned to a box.")

        box = Box.objects.select_for_update().filter(
            box_id=box_id
        ).first()

        if box is None:
            raise ValidationError("Box not found.")

        if box.status == "OCCUPIED" and box.assigned_order is not None:
            raise ValidationError("Box already has an active order.")

        box.status = "OCCUPIED"
        box.assigned_order = order
        box.assigned_at = timezone.now()
        box.released_at = None

        box.save(update_fields=[
            "status",
            "assigned_order",
            "assigned_at",
            "released_at",
            "updated_at",
        ])

        order.order_status = "BOX_ASSIGNED"
        order.save(update_fields=["order_status", "updated_at"])

        return box

    @staticmethod
    @transaction.atomic
    def get_packing_done_orders():
        order = Order.objects.filter(
            fulfillment_mode = "TAKEAWAY",
            order_status = "PACKING_DONE"
        ).order_by("created_at")
        return order

    @staticmethod
    @transaction.atomic
    def get_box_assigned_orders():
        order = Order.objects.filter(
            fulfillment_mode = "TAKEAWAY",
            order_status= "BOX_ASSIGNED"
        ).order_by("created_at")
        return order

    @staticmethod
    @transaction.atomic
    def release_box(order):

        try:
            box = Box.objects.select_for_update().get(assigned_order=order)
        except Box.DoesNotExist:
            return None

        box.status = "AVAILABLE"
        box.assigned_order = None
        box.released_at = timezone.now()

        box.save(update_fields=[
            "status",
            "assigned_order",
            "released_at",
            "updated_at",
        ])

        return box