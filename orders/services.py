from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError
from carts.services import CartService
from inventory.services import InventoryService
from payments.models import Payment
from inventory.models import Inventory
from payments.services import RefundService
from .models import *
from boxes.services import *
from notifications.services import *
from django.utils import timezone
from datetime import timedelta
import uuid
import random


class OrderService:

    @staticmethod
    def generate_order_id(order_id, fulfillment_mode):
        mode_prefix = "T" if fulfillment_mode == "TAKEAWAY" else "D"

        return (
            f"ORD-"
            f"{mode_prefix}-"
            f"{timezone.localdate().strftime('%Y%m%d')}-"
            f"{order_id:06d}"
        )

    @staticmethod
    @transaction.atomic
    def create_order(customer, payment_type, fulfillment_mode="DELIVERY"):
        cart = CartService.get_cart(customer)

        if not cart.items.exists():
            raise ValidationError("Cart is empty.")

        store = cart.store
        total_amount = Decimal("0.00")

        order = Order.objects.create(
            customer=customer,
            store=store,
            fulfillment_mode=fulfillment_mode,
            payment_status="PENDING",
            total_amount=Decimal("0.00")
        )

        order.order_id = OrderService.generate_order_id(order.id,fulfillment_mode)
        order.save(update_fields=["order_id"])

        for cart_item in cart.items.select_related("product"):
            InventoryService.reserve_stock(
                store=store,
                product=cart_item.product,
                quantity=cart_item.quantity
            )

            unit_price = cart_item.product.price
            total_price = unit_price * cart_item.quantity

            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                unit_price=unit_price,
                total_price=total_price
            )

            total_amount += total_price

        order.total_amount = total_amount

        if payment_type == "PREPAID":
            order.payment_status = "PAID"

        order.save(update_fields=[
            "total_amount",
            "payment_status",
            "updated_at"
        ])

        Payment.objects.create(
            order=order,
            payment_type=("PREPAID" if payment_type == "PREPAID" else None),
            amount=total_amount,
            status=order.payment_status
        )

        CartService.clear_cart(customer)

        return order
    
    @staticmethod
    def list_customer_orders(customer):
        return Order.objects.filter(
            customer=customer
        ).order_by("-created_at")

    @staticmethod
    def get_customer_order(customer, order_id):
        try:
            return Order.objects.prefetch_related(
                "items__product"
            ).select_related(
                "store",
                "customer"
            ).get(
                customer=customer,
                order_id=order_id
            )
        except Order.DoesNotExist:
            return None
        
    @staticmethod
    def list_packing_orders():
        return (
            Order.objects.filter(
                order_status__in=[
                    "ORDER_PLACED",
                    "PACKING_IN_PROGRESS",
                ]
            )
            .select_related(
                "customer",
                "store",
            )
            .order_by("created_at")
        )

    @staticmethod
    @transaction.atomic
    def start_packing(order_id, packer):
        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            raise ValidationError("Order not found.")

        if order.order_status != "ORDER_PLACED":
            raise ValidationError(
                "Only orders in ORDER_PLACED status can be packed."
            )

        order.order_status = "PACKING_IN_PROGRESS"
        order.packed_by = packer

        order.save(
            update_fields=[
                "order_status",
                "packed_by",
                "updated_at",
            ]
        )

        return order

    @staticmethod
    @transaction.atomic
    def complete_packing(order_id, packer):
        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            raise ValidationError("Order not found.")

        if order.order_status != "PACKING_IN_PROGRESS":
            raise ValidationError(
                "Only orders in PACKING_IN_PROGRESS status can be completed."
            )

        if order.packed_by != packer:
            raise ValidationError(
                "Only the assigned packer can complete packing."
            )

        order.order_status = "PACKING_DONE"
        order.packed_at = timezone.now()

        order.save(
            update_fields=[
                "order_status",
                "packed_at",
                "updated_at",
            ]
        )

        return order

    @staticmethod
    def get_packing_order(order_id):
        try:
            return Order.objects.prefetch_related("items").get(
                order_id=order_id
            )
        except Order.DoesNotExist:
            raise ValidationError("Order not found.")
    
    @staticmethod
    def generate_pickup_credentials(order):

        expiry_time = timezone.now() + timedelta(seconds=90)

        order.qr_token = str(uuid.uuid4())
        order.qr_expires_at = expiry_time

        order.otp = str(random.randint(1000, 9999))
        order.otp_expires_at = expiry_time

        
        if order.qr_scanned:
            order.otp_enabled = True
        else:
            order.qr_scanned = False
            order.qr_scanned_at = None
            order.otp_enabled = False

        order.otp_attempts = 0
        order.otp_verified_at = None

        order.pickup_verified = False
        order.pickup_verified_expires_at = None

        return order

    @staticmethod
    @transaction.atomic
    def mark_out_for_pickup(order_id):
        try:
            order = Order.objects.select_for_update().get(order_id=order_id)
        except Order.DoesNotExist:
            raise ValidationError("Order not found.")

        if order.fulfillment_mode != "TAKEAWAY":
            raise ValidationError("Out for pickup is only allowed for takeaway orders.")

        if order.order_status != "BOX_ASSIGNED":
            raise ValidationError("Only BOX_ASSIGNED orders can be moved out for pickup.")

        if not hasattr(order, "box"):
            raise ValidationError("Box must be assigned before moving order out for pickup.")

        order.order_status = "OUT_FOR_PICKUP"
        order.out_for_pickup_at = timezone.now()

        OrderService.generate_pickup_credentials(order)

        order.save(update_fields=[
            "order_status",
            "out_for_pickup_at",
            "qr_token",
            "qr_expires_at",
            "otp",
            "otp_expires_at",
            # "qr_scanned",
            # "qr_scanned_at",
            # "otp_enabled",
            # "otp_attempts",
            # "otp_verified_at"
            "updated_at",
        ])

        NotificationService.pickup_ready(order)

        return order
    
    @staticmethod
    @transaction.atomic
    def refresh_pickup_credentials(order_id, customer):
        try:
            order = Order.objects.select_for_update().get(
                order_id=order_id,
                customer=customer
            )
        except Order.DoesNotExist:
            raise ValidationError("Order not found.")

        if order.fulfillment_mode != "TAKEAWAY":
            raise ValidationError("Pickup credentials are only allowed for takeaway orders.")

        allowed_statuses = [
            "OUT_FOR_PICKUP",
            "VERIFICATION_IN_PROGRESS",
            "REPLACEMENT_PENDING_APPROVAL",
            "PAYMENT_PENDING",
            "READY_FOR_FINAL_HANDOVER",
        ]

        if order.order_status not in allowed_statuses:
            raise ValidationError("Pickup credentials cannot be refreshed at the current order stage.")
    
        OrderService.generate_pickup_credentials(order)

        # order.qr_scanned = False
        # order.qr_scanned_at = None
        # order.otp_enabled = False
        # order.otp_attempts = 0
        # order.otp_verified_at = None
        # order.pickup_verified = False
        # order.pickup_verified_expires_at = None

        order.save(update_fields=[
            "qr_token",
            "qr_expires_at",
            "otp",
            "otp_expires_at",
            "qr_scanned",
            "qr_scanned_at",
            "otp_enabled",
            "otp_attempts",
            "otp_verified_at",
            "pickup_verified",
            "pickup_verified_expires_at",
            "updated_at",
        ])

        return order
    
    @staticmethod
    @transaction.atomic
    def scan_qr(qr_token, staff):
        order = Order.objects.select_for_update().filter(
            qr_token=qr_token
        ).first()

        if order is None:
            raise ValidationError("Invalid QR code.")

        if order.fulfillment_mode != "TAKEAWAY":
            raise ValidationError("QR scan is only allowed for takeaway orders.")
        
        if order.qr_scanned:
            raise ValidationError("QR code has already been verified.")

        allowed_statuses = [
            "OUT_FOR_PICKUP",
            "VERIFICATION_IN_PROGRESS",
            "REPLACEMENT_PENDING_APPROVAL",
            "PAYMENT_PENDING",
            "READY_FOR_FINAL_HANDOVER",
        ]

        if order.order_status not in allowed_statuses:
            raise ValidationError("QR scanning is not allowed at the current order stage.")

        if timezone.now() > order.qr_expires_at:
            raise ValidationError("QR code has expired.")

        order.qr_scanned = True
        order.qr_scanned_at = timezone.now()
        order.otp_enabled = True
        # order.order_status = "VERIFICATION_IN_PROGRESS"

        update_fields=[
            "qr_scanned",
            "qr_scanned_at",
            "otp_enabled",
            "order_status",
            "qr_scanned",
            "qr_scanned_at",
            "otp_enabled",
            "otp_attempts",
            "otp_verified_at",
            "updated_at",
        ]

        if order.order_status == "OUT_FOR_PICKUP":
            order.order_status = "VERIFICATION_IN_PROGRESS"
            update_fields.append("order_status")

        order.save(update_fields=update_fields)

        return order
    
    @staticmethod
    def get_pickup_credentials(order_id, customer):
        try:
            order = Order.objects.get(
                order_id=order_id,
                customer=customer
            )
        except Order.DoesNotExist:
            raise ValidationError("Order not found.")

        if order.fulfillment_mode != "TAKEAWAY":
            raise ValidationError("Pickup credentials are only allowed for takeaway orders.")

        # if order.order_status not in ["OUT_FOR_PICKUP", "VERIFICATION_IN_PROGRESS"]:
        #     raise ValidationError("Pickup credentials are not available for this order.")

        allowed_statuses = [
            "OUT_FOR_PICKUP",
            "VERIFICATION_IN_PROGRESS",
            "REPLACEMENT_PENDING_APPROVAL",
            "PAYMENT_PENDING",
            "READY_FOR_FINAL_HANDOVER",
        ]

        if order.order_status not in allowed_statuses:
            raise ValidationError("Pickup credentials are not available for this order.")

        return order
    
    @staticmethod
    def get_order_for_verification(order_id):
        try:
            order = (Order.objects.select_related("box")
                .prefetch_related("items__product")
                .get(order_id=order_id)
            )
        except Order.DoesNotExist:
            raise ValidationError("Order not found.")

        if order.fulfillment_mode != "TAKEAWAY":
            raise ValidationError("Item verification is only allowed for takeaway orders.")

        if order.order_status not in ["VERIFICATION_IN_PROGRESS","REPLACEMENT_PENDING_APPROVAL",]:
            raise ValidationError("Order is not in verification stage.")

        if not order.qr_scanned:
            raise ValidationError("QR must be scanned before item verification.")

        return order
    
    @staticmethod
    @transaction.atomic
    def verify_order_item(order_id, item_id):
        order = OrderService.get_order_for_verification(order_id)

        try:
            item = order.items.get(id=item_id)
        except OrderItem.DoesNotExist:
            raise ValidationError("Order item not found.")

        if item.item_status != "ACTIVE":
            raise ValidationError("Only active items can be verified.")

        if item.is_verified:
            raise ValidationError("Item has already been verified.")

        item.is_verified = True
        item.save(update_fields=["is_verified", "updated_at"])

        return item
    
    @staticmethod
    @transaction.atomic
    def complete_item_verification(order_id):
        try:
            order = (
                Order.objects
                .select_for_update()
                .prefetch_related(
                    "items",
                    "replacement_requests",
                )
                .get(order_id=order_id)
            )
        except Order.DoesNotExist:
            raise ValidationError("Order not found.")

        if order.fulfillment_mode != "TAKEAWAY":
            raise ValidationError("Item verification is only allowed for takeaway orders.")

        if order.order_status == "REPLACEMENT_PENDING_APPROVAL":
            raise ValidationError("Pending replacement requests must be resolved before completing verification.")

        if order.order_status != "VERIFICATION_IN_PROGRESS":
            raise ValidationError("Order is not in verification stage.")

        if order.replacement_requests.filter(status="PENDING").exists():
            raise ValidationError("Pending replacement requests must be resolved before completing verification.")

        if OrderService.has_unresolved_items(order):
            raise ValidationError("All active items must be verified or cancelled before completing verification.")

        active_items_exist = order.items.filter(item_status="ACTIVE").exists()

        if not active_items_exist:
            raise ValidationError("Order has no active items available for handover.")

        order.verification_completed = True

        if order.payment_status == "PAID":
            order.order_status = "READY_FOR_FINAL_HANDOVER"
        else:
            order.order_status = "PAYMENT_PENDING"

        order.save(
            update_fields=[
                "verification_completed",
                "order_status",
                "updated_at",
            ]
        )

        return order
    
    @staticmethod
    def recalculate_order_total(order):
        total_amount = Decimal("0.00")

        active_items = order.items.filter(item_status="ACTIVE")

        for item in active_items:
            total_amount += item.total_price

        order.total_amount = total_amount
        order.save(update_fields=["total_amount", "updated_at"])

        return order
    
    @staticmethod
    @transaction.atomic
    def cancel_order_item(order_id, item_id, reason):
        order = OrderService.get_order_for_verification(order_id)

        try:
            item = order.items.get(id=item_id)
        except OrderItem.DoesNotExist:
            raise ValidationError("Order item not found.")

        if item.item_status != "ACTIVE":
            raise ValidationError("Only active items can be cancelled.")

        if item.is_verified:
            raise ValidationError("Verified items cannot be cancelled.")

        item.item_status = "CANCELLED"
        item.is_verified = False
        item.cancellation_reason = reason

        item.save(update_fields=[
            "item_status",
            "is_verified",
            "cancellation_reason",
            "updated_at",
        ])

        OrderService.recalculate_order_total(order)

        RefundService.create_item_refund(order_item=item,reason=reason,)

        OrderService.cancel_order_if_no_active_items(order)

        active_items_exists = order.items.filter(item_status="ACTIVE").exists()

        if not active_items_exists:
            order.order_status = "ORDER_CANCELLED"
            order.cancelled_at = timezone.now()
            order.save(update_fields=[
                "order_status",
                "cancelled_at",
                "updated_at",
            ])

            if hasattr(order, "box"):
                box = order.box
                box.status = "AVAILABLE"
                box.assigned_order = None
                box.released_at = timezone.now()
                box.save(update_fields=[
                    "status",
                    "assigned_order",
                    "released_at",
                    "updated_at",
                ])

        return item
    
    @staticmethod
    @transaction.atomic
    def request_replacement(order_id, item_id, requested_by, reason):
        try:
            order = Order.objects.select_for_update().get(order_id=order_id)
        except Order.DoesNotExist:
            raise ValidationError("Order not found.")

        if order.fulfillment_mode != "TAKEAWAY":
            raise ValidationError("Replacement is only allowed for takeaway orders.")

        if order.order_status not in ["VERIFICATION_IN_PROGRESS","REPLACEMENT_PENDING_APPROVAL",]:
            raise ValidationError("Replacement request is not allowed at the current order stage.")

        if not order.qr_scanned:
            raise ValidationError("QR must be scanned before requesting replacement.")

        try:
            item = order.items.get(id=item_id)
        except OrderItem.DoesNotExist:
            raise ValidationError("Order item not found.")

        if item.item_status != "ACTIVE":
            raise ValidationError("Only active items can be replaced.")

        if item.is_verified:
            raise ValidationError("Verified items cannot be replaced.")

        if item.replacement_requests.filter(status="PENDING").exists():
            raise ValidationError("A replacement request is already pending for this item.")

        replacement_request = ReplacementRequest.objects.create(
            order=order,
            order_item=item,
            requested_by=requested_by,
            reason=reason,
            status="PENDING",
        )

        if order.order_status != "REPLACEMENT_PENDING_APPROVAL":
            order.order_status = "REPLACEMENT_PENDING_APPROVAL"
            order.save(update_fields=["order_status", "updated_at"])

        return replacement_request

    @staticmethod
    @transaction.atomic
    def approve_replacement(replacement_request_id, supervisor, supervisor_note=""):
        try:
            replacement_request = (
                ReplacementRequest.objects
                .select_for_update(of=("self",))
                .select_related("order", "order_item", "replacement_product")
                .get(id=replacement_request_id)
            )
        except ReplacementRequest.DoesNotExist:
            raise ValidationError("Replacement request not found.")

        if replacement_request.status != "PENDING":
            raise ValidationError("Replacement request has already been decided.")

        order = replacement_request.order
        order_item = replacement_request.order_item
        product = order_item.product

        try:
            inventory = (
                Inventory.objects
                .select_for_update()
                .get(
                    store=order.store,
                    product=product,
                )
            )
        except Inventory.DoesNotExist:
            raise ValidationError(
                "Inventory record not found for this product."
            )

        if inventory.available_quantity < order_item.quantity:
            raise ValidationError(
                "Insufficient stock available for this item."
            )

        replacement_request.status = "APPROVED"
        replacement_request.decided_by = supervisor
        replacement_request.supervisor_note = supervisor_note
        replacement_request.decided_at = timezone.now()

        replacement_request.save(update_fields=[
            "status",
            "decided_by",
            "supervisor_note",
            "decided_at",
            "updated_at",
        ])

        OrderService.update_order_after_replacement_decision(replacement_request.order)

        NotificationService.replacement_approved(replacement_request)

        return replacement_request

    @staticmethod
    @transaction.atomic
    def reject_replacement(replacement_request_id, supervisor, supervisor_note=""):
        try:
            replacement_request = (
                ReplacementRequest.objects
                .select_for_update(of=("self",))
                .select_related("order", "order_item")
                .get(id=replacement_request_id)
            )
        except ReplacementRequest.DoesNotExist:
            raise ValidationError("Replacement request not found.")

        if replacement_request.status != "PENDING":
            raise ValidationError("Replacement request has already been decided.")

        if not supervisor_note or not supervisor_note.strip():
            raise ValidationError("Supervisor note is required when rejecting a replacement request.")

        replacement_request.status = "REJECTED"
        replacement_request.decided_by = supervisor
        replacement_request.supervisor_note = supervisor_note
        replacement_request.decided_at = timezone.now()
        replacement_request.save(update_fields=[
            "status",
            "decided_by",
            "supervisor_note",
            "decided_at",
            "updated_at",
        ])

        order_item = replacement_request.order_item
        order_item.item_status = "CANCELLED"
        order_item.is_verified = False
        order_item.cancellation_reason = "REPLACEMENT_REJECTED"
        order_item.save(update_fields=[
            "item_status",
            "is_verified",
            "cancellation_reason",
            "updated_at",
        ])

        order = replacement_request.order

        # remaining_items = order.items.filter(item_status="ACTIVE").exists()

        # if remaining_items:
        #     order.order_status = "VERIFICATION_IN_PROGRESS"
        # else:
        #     order.order_status = "CANCELLED"

        # order.save(update_fields=["order_status","updated_at",])

        OrderService.recalculate_order_total(replacement_request.order)
        OrderService.update_order_after_replacement_decision(order)
        
        NotificationService.replacement_rejected(replacement_request)

        return replacement_request

    @staticmethod
    def get_pending_replacement_requests():

        return (
            ReplacementRequest.objects
            .filter(status="PENDING")
            .select_related(
                "order",
                "order_item",
                "order_item__product",
                "requested_by",
            )
            .order_by("-created_at")
        )

    @staticmethod
    def get_replacement_request_detail(replacement_request_id):

        try:
            replacement_request = (
                ReplacementRequest.objects
                .select_related(
                    "order",
                    "order_item",
                    "order_item__product",
                    "requested_by",
                    "decided_by",
                )
                .get(id=replacement_request_id)
            )

        except ReplacementRequest.DoesNotExist:
            raise ValidationError("Replacement request not found.")

        order = replacement_request.order
        order_item = replacement_request.order_item
        product = order_item.product

        try:
            inventory = Inventory.objects.get(
                store=order.store,
                product=product,
            )

            available_quantity = inventory.available_quantity

        except Inventory.DoesNotExist:
            available_quantity = 0
        
        history = (ReplacementRequest.objects.filter(order=replacement_request.order).select_related("order_item","order_item__product",).order_by("created_at"))

        return {
            "current_request": replacement_request,
            "replacement_history": history,
            "available_quantity": available_quantity,
        }
    
    @staticmethod
    def update_order_after_replacement_decision(order):

        pending_requests_exist = order.replacement_requests.filter(status="PENDING").exists()

        active_items_exist = order.items.filter(item_status="ACTIVE").exists()

        if not active_items_exist:
            order.order_status = "CANCELLED"

        elif pending_requests_exist:
            order.order_status = "REPLACEMENT_PENDING_APPROVAL"

        else:
            order.order_status = "VERIFICATION_IN_PROGRESS"

        order.save(update_fields=["order_status","updated_at",])

        return order
    
    @staticmethod
    def has_unresolved_items(order):
        active_items = order.items.filter(
            item_status="ACTIVE")

        for item in active_items:
            if not item.is_verified:
                return True

        return False
        
    @staticmethod
    def cancel_order_if_no_active_items(order):
        active_items_exist = order.items.filter(item_status="ACTIVE").exists()

        if active_items_exist:
            return False

        # order.order_status = "ORDER_CANCELLED"
        # order.cancelled_at = timezone.now()

        # order.save(
        #     update_fields=[
        #         "order_status",
        #         "cancelled_at",
        #         "updated_at",
        #     ]
        # )

        # BoxService.release_box(order)

        OrderService.cancel_order(order=order,reason="ALL_ITEMS_CANCELLED",restore_inventory=False,release_box=True,)

        return True
    
    @staticmethod
    @transaction.atomic
    def verify_pickup_otp(order_id, otp):
        try:
            order = Order.objects.select_for_update().get(order_id=order_id)
        except Order.DoesNotExist:
            raise ValidationError("Order not found.")

        if order.fulfillment_mode != "TAKEAWAY":
            raise ValidationError("OTP verification is only allowed for takeaway orders.")

        if order.order_status != "READY_FOR_FINAL_HANDOVER":
            raise ValidationError("Order is not ready for final handover.")

        if not order.otp_enabled:
            raise ValidationError("OTP is not enabled. Scan the latest QR code first.")

        if order.otp_verified_at is not None:
            raise ValidationError("OTP has already been verified.")

        if order.otp_expires_at is None or timezone.now() > order.otp_expires_at:
            raise ValidationError("OTP has expired. Refresh credentials and scan the new QR code.")

        if order.otp_attempts >= 5:
            raise ValidationError("Maximum OTP attempts exceeded. Refresh pickup credentials.")

        if str(order.otp) != str(otp).strip():
            order.otp_attempts += 1
            order.save(update_fields=["otp_attempts","updated_at",])

            remaining_attempts = 5 - order.otp_attempts

            if remaining_attempts == 0:
                raise ValidationError("Maximum OTP attempts exceeded. Refresh pickup credentials.")

            raise ValidationError(f"Invalid OTP. {remaining_attempts} attempts remaining.")

        order.otp_verified_at = timezone.now()

        order.pickup_verified = True

        order.pickup_verified_expires_at = (timezone.now() + timedelta(minutes=5))

        order.save(
            update_fields=[
                "otp_verified_at",
                "pickup_verified",
                "pickup_verified_expires_at",
                "updated_at",
            ]
        )

        return order
    
    @staticmethod
    @transaction.atomic
    def complete_pickup(order_id, takeaway_staff):
        try:
            order = (Order.objects
                .select_for_update()
                .select_related("customer", "store")
                .get(order_id=order_id))
        except Order.DoesNotExist:
            raise ValidationError("Order not found.")

        if order.fulfillment_mode != "TAKEAWAY":
            raise ValidationError("Pickup completion is only allowed for takeaway orders.")

        if order.order_status != "READY_FOR_FINAL_HANDOVER":
            raise ValidationError("Order is not ready for final handover.")

        if order.payment_status != "PAID":
            raise ValidationError("Payment must be completed before pickup.")

        if not order.pickup_verified:
            raise ValidationError("Pickup verification has not been completed.")

        if (order.pickup_verified_expires_at is None or timezone.now() > order.pickup_verified_expires_at):
            raise ValidationError("Pickup verification has expired. Please verify OTP again.")

        try:
            payment = Payment.objects.get(order=order)
        except Payment.DoesNotExist:
            raise ValidationError("Payment record not found for this order.")

        box = getattr(order, "box", None)

        PickupHistory.objects.create(
            order=order,
            customer=order.customer,
            takeaway_staff=takeaway_staff,
            box=box,
            payment_type=payment.payment_type,
            payment_amount=payment.amount,
            qr_scanned_at=order.qr_scanned_at,
            otp_verified_at=order.otp_verified_at)

        order.order_status = "PICKED_UP"
        order.picked_up_at = timezone.now()

        order.qr_token = None
        order.qr_expires_at = None
        order.qr_scanned = False
        order.qr_scanned_at = None

        order.otp = None
        order.otp_expires_at = None
        order.otp_enabled = False
        order.otp_attempts = 0
        order.otp_verified_at = None

        order.pickup_verified = False
        order.pickup_verified_expires_at = None

        order.save(
            update_fields=[
                "order_status",
                "picked_up_at",
                "qr_token",
                "qr_expires_at",
                "qr_scanned",
                "qr_scanned_at",
                "otp",
                "otp_expires_at",
                "otp_enabled",
                "otp_attempts",
                "otp_verified_at",
                "pickup_verified",
                "pickup_verified_expires_at",
                "updated_at",
            ]
        )

        BoxService.release_box(order)

        NotificationService.pickup_completed(order)

        return order
    
    @staticmethod
    @transaction.atomic
    def get_payment_summary(order_id):
        try:
            order = (Order.objects.select_related("payment").get(order_id=order_id))
        except Order.DoesNotExist:
            raise ValidationError("Order not found.")

        if order.fulfillment_mode != "TAKEAWAY":
            raise ValidationError("Payment summary is only available for takeaway orders.")

        if not order.qr_scanned:
            raise ValidationError("QR must be scanned before viewing payment summary.")

        if order.replacement_requests.filter(status="PENDING").exists():
            raise ValidationError("Pending replacement requests must be resolved first.")

        if OrderService.has_unresolved_items(order):
            raise ValidationError("All active items must be verified or cancelled first.")

        if not order.verification_completed:
            raise ValidationError("Item verification must be completed first.")

        if order.order_status not in ["PAYMENT_PENDING","READY_FOR_FINAL_HANDOVER",]:
            raise ValidationError("Payment summary is not available at the current order stage.")

        return order
    
    @staticmethod
    @transaction.atomic
    def cancel_timed_out_order(order_id):
        try:
            order = (
                Order.objects
                .select_for_update()
                .select_related("store")
                .get(id=order_id)
            )
        except Order.DoesNotExist:
            return False

        if order.fulfillment_mode != "TAKEAWAY":
            return False

        if order.order_status != "OUT_FOR_PICKUP":
            return False

        if order.out_for_pickup_at is None:
            return False

        timeout_at = order.out_for_pickup_at + timedelta(minutes=30)

        if timezone.now() <= timeout_at:
            return False

        # active_items = (order.items.select_related("product").filter(item_status="ACTIVE"))

        # for item in active_items:
        #     inventory = (Inventory.objects.select_for_update().filter(store=order.store,product=item.product).first())

        #     if inventory is None:
        #         raise ValidationError(f"Inventory not found for {item.product.product_name}.")

        #     if inventory.reserved_quantity < item.quantity:
        #         raise ValidationError(
        #             f"Reserved stock is insufficient for "
        #             f"{item.product.product_name}.")

        #     inventory.available_quantity += item.quantity
        #     inventory.reserved_quantity -= item.quantity

        #     inventory.save(update_fields=[
        #             "available_quantity",
        #             "reserved_quantity",
        #             "updated_at",])

        # order.order_status = "ORDER_CANCELLED"
        # order.cancelled_at = timezone.now()

        # order.save(update_fields=[
        #         "order_status",
        #         "cancelled_at",
        #         "updated_at",])

        # BoxService.release_box(order)

        OrderService.cancel_order(order=order,reason="PICKUP_TIMEOUT",restore_inventory=True,release_box=True,process_refund=True)

        return True
    
    @staticmethod
    @transaction.atomic
    def cancel_order(order,reason,restore_inventory=True,release_box=True,process_refund=False):

        order = Order.objects.select_for_update().get(id=order.id)

        if order.order_status in ["ORDER_CANCELLED", "PICKED_UP"]:
            raise ValidationError("Order cannot be cancelled at the current stage.")

        if restore_inventory:
            for item in order.items.select_related("product").filter(item_status="ACTIVE"):
                inventory = (Inventory.objects.select_for_update().filter(store=order.store,product=item.product,).first())

                if inventory:
                    inventory.available_quantity += item.quantity
                    inventory.reserved_quantity = max(0,inventory.reserved_quantity - item.quantity,)

                    inventory.save(update_fields=[
                        "available_quantity",
                        "reserved_quantity",
                        "updated_at",])

        order.order_status = "ORDER_CANCELLED"
        order.cancelled_at = timezone.now()
        order.cancellation_reason = reason

        order.save(update_fields=[
                "order_status",
                "cancelled_at",
                # "cancellation_reason",
                "updated_at",])

        if release_box:
            BoxService.release_box(order)

        if process_refund:
            RefundService.create_full_refund(order=order,reason=reason,)

        NotificationService.order_cancelled( order=order,reason=reason,)

        return order

    @staticmethod
    @transaction.atomic
    def get_pickup_status(order_id):
        try:
            order = Order.objects.get(
                order_id=order_id
            )
        except Order.DoesNotExist:
            raise ValidationError("Order not found.")

        if order.fulfillment_mode != "TAKEAWAY":
            raise ValidationError(
                "Pickup status is only available for takeaway orders."
            )

        return order

    