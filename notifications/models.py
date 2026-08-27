from django.db import models
from django.conf import settings

# Create your models here.
class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='notifications')
    order = models.ForeignKey("orders.Order",on_delete=models.CASCADE,null=True,blank=True,related_name="notifications",)
    title = models.CharField(max_length=255)
    message = models.TextField()
    NOTIFICATION_TYPE_CHOICES = [
        ("PICKUP_READY", "Pickup Ready"),
        ("ORDER_CANCELLED", "Order Cancelled"),
        ("REPLACEMENT_APPROVED", "Replacement Approved"),
        ("REPLACEMENT_REJECTED", "Replacement Rejected"),
        ("PAYMENT_RECEIVED", "Payment Received"),
        ("REFUND_INITIATED", "Refund Initiated"),
        ("REFUND_COMPLETED", "Refund Completed"),
        ("PICKUP_COMPLETED", "Pickup Completed"),
    ]
    # notification_type = models.CharField(max_length=40,choices=NOTIFICATION_TYPE_CHOICES,default="PICKUP_READY")
    notification_type = models.CharField(max_length=40,choices=NOTIFICATION_TYPE_CHOICES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
