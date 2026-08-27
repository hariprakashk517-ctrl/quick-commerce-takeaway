from django.core.exceptions import ValidationError
from django.db import transaction
from decimal import Decimal
from django.utils import timezone
from orders.models import Order
from .models import *
from notifications.services import *


class PaymentService:

    @staticmethod
    @transaction.atomic
    def collect_payment(order_id,payment_type,collected_by,transaction_id=""):
        try:
            order = (
                Order.objects
                .select_for_update()
                .select_related("store")
                .get(order_id=order_id)
            )
        except Order.DoesNotExist:
            raise ValidationError("Order not found.")

        if order.fulfillment_mode != "TAKEAWAY":
            raise ValidationError("Pickup payment collection is only allowed for takeaway orders.")

        if order.order_status != "PAYMENT_PENDING":
            raise ValidationError("Payment can be collected only when the order is in PAYMENT_PENDING status.")

        if not order.verification_completed:
            raise ValidationError("Item verification must be completed before collecting payment.")

        if order.payment_status == "PAID":
            raise ValidationError("Payment has already been completed.")

        if payment_type not in ["CASH_ON_PICKUP","UPI_ON_PICKUP","CARD_ON_PICKUP",]:
            raise ValidationError("Invalid pickup payment type.")

        transaction_id = transaction_id.strip()

        if (payment_type in ["UPI_ON_PICKUP", "CARD_ON_PICKUP"] and not transaction_id):
            raise ValidationError("Transaction ID is required for UPI and card payments.")

        try:
            payment = Payment.objects.select_for_update().get(order=order)
        except Payment.DoesNotExist:
            raise ValidationError("Payment record not found for this order.")

        payment.payment_type = payment_type
        payment.amount = order.total_amount
        payment.status = "PAID"
        payment.transaction_id = (transaction_id if transaction_id else None)
        payment.collected_by = collected_by
        payment.paid_at = timezone.now()

        payment.save(
            update_fields=[
                "payment_type",
                "amount",
                "status",
                "transaction_id",
                "collected_by",
                "paid_at",
                "updated_at",
            ]
        )

        if payment_type == "CASH_ON_PICKUP":
            CashLedger.objects.get_or_create(
                payment=payment,
                defaults={
                    "store": order.store,
                    "amount": payment.amount,
                    "collected_by": collected_by,
                    "status": "PENDING_HANDOVER",
                }
            )

        order.payment_status = "PAID"
        order.order_status = "READY_FOR_FINAL_HANDOVER"

        order.save(
            update_fields=[
                "payment_status",
                "order_status",
                "updated_at",
            ]
        )

        NotificationService.payment_received(order)

        return payment
    
    @staticmethod
    @transaction.atomic
    def handover_cash(order_id, supervisor, supervisor_note=""):
        try:
            payment = (Payment.objects.select_for_update().select_related("cash_ledger", "order").get(order__order_id=order_id))
        except Payment.DoesNotExist:
            raise ValidationError("Payment not found.")

        if payment.payment_type != "CASH_ON_PICKUP":
            raise ValidationError("Cash handover is only available for cash payments.")

        try:
            cash_ledger = payment.cash_ledger
        except CashLedger.DoesNotExist:
            raise ValidationError("Cash ledger record not found.")

        if cash_ledger.status == "HANDED_OVER":
            raise ValidationError("Cash has already been handed over.")

        if cash_ledger.status != "PENDING_HANDOVER":
            raise ValidationError("Cash handover is not allowed at the current stage.")

        cash_ledger.handed_over_to = supervisor
        cash_ledger.handed_over_at = timezone.now()
        cash_ledger.supervisor_note = supervisor_note
        cash_ledger.status = "HANDED_OVER"

        cash_ledger.save(
            update_fields=[
                "handed_over_to",
                "handed_over_at",
                "supervisor_note",
                "status",
                "updated_at",
            ]
        )

        return cash_ledger
    
class RefundService:

    @staticmethod
    @transaction.atomic
    def create_full_refund(order, reason):
        try:
            payment = Payment.objects.select_for_update().get(order=order)
        except Payment.DoesNotExist:
            raise ValidationError("Payment record not found.")

        if payment.status != "PAID":
            return None

        existing_refund = Refund.objects.filter(order=order,order_item__isnull=True,status__in=["PENDING", "IN_PROGRESS", "COMPLETED"],).first()

        if existing_refund:
            return existing_refund

        refund = Refund.objects.create(
            order=order,
            order_item=None,
            amount=payment.amount,
            status="IN_PROGRESS",
            reason=reason,)

        order.refund_status = "REFUND_IN_PROGRESS"
        order.save(update_fields=[
                "refund_status",
                "updated_at",])
        
        NotificationService.refund_initiated(refund)

        return refund

    @staticmethod
    @transaction.atomic
    def create_item_refund(order_item, reason):
        order = order_item.order

        try:
            payment = Payment.objects.select_for_update().get(order=order)
        except Payment.DoesNotExist:
            raise ValidationError("Payment record not found.")

        if payment.status != "PAID":
            return None

        existing_refund = Refund.objects.filter(order=order,order_item=order_item,).first()

        if existing_refund:
            return existing_refund

        refund = Refund.objects.create(
            order=order,
            order_item=order_item,
            amount=order_item.total_price,
            status="IN_PROGRESS",
            reason=reason,)

        order.refund_status = "REFUND_IN_PROGRESS"

        order.save(update_fields=[
                "refund_status",
                "updated_at",])
        
        NotificationService.refund_initiated(refund)

        return refund
    
    @staticmethod
    @transaction.atomic
    def complete_refund(refund_id):
        try:
            refund = (Refund.objects.select_for_update().select_related("order").get(id=refund_id))
        except Refund.DoesNotExist:
            raise ValidationError("Refund not found.")

        if refund.status == "COMPLETED":
            raise ValidationError("Refund has already been completed.")

        if refund.status != "IN_PROGRESS":
            raise ValidationError("Only refunds in IN_PROGRESS status can be completed.")

        refund.status = "COMPLETED"
        refund.processed_at = timezone.now()

        refund.save(update_fields=[
                "status",
                "processed_at",
                "updated_at",])

        order = refund.order

        failed_refunds_exist = order.refunds.filter(status="FAILED").exists()

        unfinished_refunds_exist = order.refunds.filter(status__in=["PENDING", "IN_PROGRESS"]).exists()

        if failed_refunds_exist:
            order.refund_status = "REFUND_FAILED"

        elif not unfinished_refunds_exist:
            order.refund_status = "REFUND_COMPLETED"

        else:
            order.refund_status = "REFUND_IN_PROGRESS"

        order.save(update_fields=[
                "refund_status",
                "updated_at",])
        
        NotificationService.refund_completed(refund)

        return refund
    
    # @staticmethod
    # @transaction.atomic
    # def complete_refund(refund_id):
    #     try:
    #         refund = (Refund.objects
    #             .select_for_update()
    #             .select_related("order")
    #             .get(id=refund_id))
    #     except Refund.DoesNotExist:
    #         raise ValidationError("Refund not found.")

    #     if refund.status == "COMPLETED":
    #         raise ValidationError("Refund has already been completed.")

    #     if refund.status != "IN_PROGRESS":
    #         raise ValidationError("Only refunds in IN_PROGRESS status can be completed.")

    #     refund.status = "COMPLETED"
    #     refund.processed_at = timezone.now()

    #     refund.save(update_fields=[
    #             "status",
    #             "processed_at",
    #             "updated_at",])

    #     order = refund.order

    #     failed_refunds_exist = order.refunds.filter(status="FAILED").exists()

    #     unfinished_refunds_exist = order.refunds.filter(status__in=["PENDING", "IN_PROGRESS"]).exists()

    #     if failed_refunds_exist:
    #         order.refund_status = "REFUND_FAILED"

    #     elif not unfinished_refunds_exist:
    #         order.refund_status = "REFUND_COMPLETED"

    #     else:
    #         order.refund_status = "REFUND_IN_PROGRESS"

    #     order.save(update_fields=[
    #             "refund_status",
    #             "updated_at",])

    #     return refund
    
