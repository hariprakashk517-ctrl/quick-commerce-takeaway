from .models import Notification


class NotificationService:

    @staticmethod
    def create_notification(recipient,notification_type,title,message,order=None,):
        return Notification.objects.create(recipient=recipient,order=order,notification_type=notification_type,title=title,message=message,)
    
    @staticmethod
    def pickup_ready(order):
        return NotificationService.create_notification(
            recipient=order.customer,
            order=order,
            notification_type="PICKUP_READY",
            title="Order Ready for Pickup",
            message=f"Your order {order.order_id} is ready for pickup.",
        )
    
    @staticmethod
    def order_cancelled(order, reason=None):
        if reason == "PICKUP_TIMEOUT":
            message = (
                f"Your order {order.order_id} was cancelled because "
                f"it was not collected within 30 minutes."
            )
        else:
            message = f"Your order {order.order_id} has been cancelled."

        return NotificationService.create_notification(
            recipient=order.customer,
            order=order,
            notification_type="ORDER_CANCELLED",
            title="Order Cancelled",
            message=message,
        )
    
    @staticmethod
    def replacement_approved(replacement_request):
        order = replacement_request.order

        return NotificationService.create_notification(
            recipient=order.customer,
            order=order,
            notification_type="REPLACEMENT_APPROVED",
            title="Replacement Approved",
            message=(
                f"Your replacement request for order "
                f"{order.order_id} has been approved."
            ),
        )

    @staticmethod
    def replacement_rejected(replacement_request):
        order = replacement_request.order

        return NotificationService.create_notification(
            recipient=order.customer,
            order=order,
            notification_type="REPLACEMENT_REJECTED",
            title="Replacement Rejected",
            message=(
                f"Your replacement request for order "
                f"{order.order_id} has been rejected."
            ),
        )
    
    @staticmethod
    def payment_received(order):
        return NotificationService.create_notification(
            recipient=order.customer,
            order=order,
            notification_type="PAYMENT_RECEIVED",
            title="Payment Received",
            message=(
                f"Payment for order {order.order_id} "
                f"has been received successfully."
            ),
        )

    @staticmethod
    def refund_initiated(refund):
        order = refund.order

        return NotificationService.create_notification(
            recipient=order.customer,
            order=order,
            notification_type="REFUND_INITIATED",
            title="Refund Initiated",
            message=(
                f"A refund of ₹{refund.amount} for order "
                f"{order.order_id} has been initiated."
            ),
        )

    @staticmethod
    def refund_completed(refund):
        order = refund.order

        return NotificationService.create_notification(
            recipient=order.customer,
            order=order,
            notification_type="REFUND_COMPLETED",
            title="Refund Completed",
            message=(
                f"Your refund of ₹{refund.amount} for order "
                f"{order.order_id} has been completed."
            ),
        )
    
    @staticmethod
    def pickup_completed(order):
        return NotificationService.create_notification(
            recipient=order.customer,
            order=order,
            notification_type="PICKUP_COMPLETED",
            title="Pickup Completed",
            message=(
                f"Your order {order.order_id} "
                f"has been collected successfully."
            ),
        )
    
    @staticmethod
    def list_user_notifications(user):
        return Notification.objects.filter(recipient=user).order_by("-created_at")

    @staticmethod
    def mark_notification_as_read(notification_id, user):
        try:
            notification = Notification.objects.get(
                id=notification_id,
                recipient=user)
        except Notification.DoesNotExist:
            return None

        if not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=[
                    "is_read",
                    "updated_at",])

        return notification

    @staticmethod
    def mark_all_as_read(user):
        return Notification.objects.filter(recipient=user,is_read=False).update(is_read=True)