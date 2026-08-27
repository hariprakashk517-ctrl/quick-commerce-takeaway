from django.db import models
from django.conf import settings


class Order(models.Model):
    order_id = models.CharField(max_length=30, unique=True,null=True,blank=True, editable=False)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="orders")
    store = models.ForeignKey('stores.Store', on_delete=models.CASCADE,related_name="orders")
    ORDER_STATUS_CHOICES = [
    ('ORDER_PLACED', 'ORDER_PLACED'),
    ('PACKING_IN_PROGRESS', 'PACKING_IN_PROGRESS'),
    ('PACKING_DONE', 'PACKING_DONE'),
    ('BOX_ASSIGNED', 'BOX_ASSIGNED'),
    ('MARK_OUT_FOR_DELIVERY', 'MARK_OUT_FOR_DELIVERY'),
    ('OUT_FOR_PICKUP', 'OUT_FOR_PICKUP'),
    ('VERIFICATION_IN_PROGRESS', 'VERIFICATION_IN_PROGRESS'),
    ('REPLACEMENT_PENDING_APPROVAL', 'REPLACEMENT_PENDING_APPROVAL'),
    ('PAYMENT_PENDING', 'PAYMENT_PENDING'),
    ('READY_FOR_FINAL_HANDOVER', 'READY_FOR_FINAL_HANDOVER'),
    ('PICKED_UP', 'PICKED_UP'),
    ('ORDER_CANCELLED', 'ORDER_CANCELLED'),
    ]
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='ORDER_PLACED')
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'PENDING'),
        ('PAID', 'PAID'),
        ('FAILED', 'FAILED'),
        ('REFUNDED', 'REFUNDED'),
        ('PARTIALLY_REFUNDED', 'PARTIALLY_REFUNDED'),
    ]
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    REFUND_STATUS_CHOICES = [
        ('NOT_REQUIRED', 'NOT_REQUIRED'),
        ('REFUND_IN_PROGRESS', 'REFUND_IN_PROGRESS'),
        ('REFUND_COMPLETED', 'REFUND_COMPLETED'),
        ('REFUND_FAILED', 'REFUND_FAILED'),
    ]
    refund_status = models.CharField(max_length=20, choices=REFUND_STATUS_CHOICES, default='NOT_REQUIRED')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    qr_token = models.CharField(max_length=255,null=True,blank=True)
    qr_expires_at = models.DateTimeField(null=True,blank=True)
    otp = models.CharField(max_length=4,null=True,blank=True)
    otp_expires_at = models.DateTimeField(null=True,blank=True)
    otp_enabled = models.BooleanField(null=True,blank=True,default=False)
    out_for_pickup_at = models.DateTimeField(null=True,blank=True)
    picked_up_at = models.DateTimeField(null=True,blank=True)
    cancelled_at = models.DateTimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    FULFILLMENT_MODE_CHOICES = [
    ('DELIVERY', 'DELIVERY'),
    ('TAKEAWAY', 'TAKEAWAY'),]
    fulfillment_mode = models.CharField(max_length=20,choices=FULFILLMENT_MODE_CHOICES,default='DELIVERY')
    customer_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    customer_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    distance_from_store_km = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    packed_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='packed_orders')
    packed_at = models.DateTimeField(null=True, blank=True)
    qr_scanned = models.BooleanField(default=False)
    qr_scanned_at = models.DateTimeField(null=True, blank=True)
    verification_completed = models.BooleanField(default=False)
    replacement_resolved = models.BooleanField(default=True)
    otp_attempts = models.PositiveSmallIntegerField(default=0)
    otp_verified_at = models.DateTimeField(null=True, blank=True)
    pickup_verified = models.BooleanField(default=False)
    pickup_verified_expires_at = models.DateTimeField(null=True,blank=True)
    PAYMENT_TYPE_CHOICES = [
    ("PREPAID", "Prepaid"),
    ("PAY_AT_TAKEAWAY", "Pay at Takeaway"),
    ]
    payment_type = models.CharField(max_length=20,choices=PAYMENT_TYPE_CHOICES,default="PREPAID",)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey('products.Product',on_delete=models.CASCADE,related_name='order_items')
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10,decimal_places=2)
    total_price = models.DecimalField(max_digits=10,decimal_places=2)
    ITEM_STATUS_CHOICES = [
    ('ACTIVE', 'ACTIVE'),
    ('CANCELLED', 'CANCELLED'),
    ('REPLACED', 'REPLACED'),
    ]
    item_status = models.CharField(max_length=20,choices=ITEM_STATUS_CHOICES,default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    CANCELLATION_REASONS = [
    ("WRONG_ITEM", "Wrong Item Packed"),
    ("DAMAGED_ITEM", "Damaged Item"),
    ("ITEM_MISSING", "Item Missing"),
    ("CUSTOMER_DECLINED", "Customer Declined Item"),
    ("QUALITY_ISSUE", "Quality Issue"),
    ("OTHER", "Other"),]
    cancellation_reason = models.CharField(max_length=30,choices=CANCELLATION_REASONS,blank=True,null=True)

class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="status_history")
    old_status = models.CharField(max_length=50)
    new_status = models.CharField(max_length=50)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    note = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# class ReplacementRequest(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='replacement_requests')
#     order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='replacement_requests')
#     requested_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name='replacement_requests_created')
#     approved_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='replacement_requests_approved')
#     reason = models.TextField()
#     STATUS_CHOICES = [
#         ('PENDING', 'PENDING'),
#         ('APPROVED', 'APPROVED'),
#         ('REJECTED', 'REJECTED'),
#     ]
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
#     replacement_product = models.ForeignKey('products.Product',on_delete=models.SET_NULL,null=True,blank=True,related_name='replacement_requests')
#     replacement_quantity = models.PositiveIntegerField(default=1)
#     decision_note = models.TextField(null=True, blank=True)
#     decided_at = models.DateTimeField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

class PickupCompletion(models.Model):
    pickup_completion_id = models.CharField(max_length=30, unique=True, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='pickup_completion')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='pickup_completions')
    packer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='packed_pickup_completions')
    takeaway_staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='handled_pickups')
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='supervised_pickups')
    box_id = models.CharField(max_length=20, null=True, blank=True)
    qr_scan_status = models.BooleanField(default=False)
    qr_scan_time = models.DateTimeField(null=True, blank=True)
    otp_verified_status = models.BooleanField(default=False)
    otp_verification_time = models.DateTimeField(null=True, blank=True)
    payment_status = models.CharField(max_length=30)
    payment_mode = models.CharField(max_length=30, null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    refunded_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cancelled_items = models.JSONField(default=list, blank=True)
    replaced_items = models.JSONField(default=list, blank=True)
    replacement_reasons = models.JSONField(default=list, blank=True)
    supervisor_decision = models.CharField(max_length=50, null=True, blank=True)
    picked_up_at = models.DateTimeField()
    final_order_status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class TimeoutCancellation(models.Model):
    cancellation_id = models.CharField(max_length=30, unique=True, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='timeout_cancellation')
    reason = models.CharField(max_length=100, default='pickup timeout > 30 min')
    out_for_pickup_at = models.DateTimeField()
    cancelled_at = models.DateTimeField()
    item_wise_stock_restored_details = models.JSONField(default=list, blank=True)
    refund_initiated = models.BooleanField(default=False)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    box_released = models.BooleanField(default=False)
    notification_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class ReplacementRequest(models.Model):
    REQUEST_STATUS_CHOICES = [
        ("PENDING", "PENDING"),
        ("APPROVED", "APPROVED"),
        ("REJECTED", "REJECTED"),
    ]
    REPLACEMENT_REASON_CHOICES = [
        ("DAMAGED_ITEM", "Damaged Item"),
        ("WRONG_ITEM", "Wrong Item Packed"),
        ("QUALITY_ISSUE", "Quality Issue"),
        ("PACKAGING_DAMAGE", "Packaging Damage"),
        ("ITEM_MISSING", "Item Missing"),
        ("OTHER", "Other"),
    ]
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="replacement_requests")
    order_item = models.ForeignKey(OrderItem,on_delete=models.CASCADE,related_name="replacement_requests")
    replacement_product = models.ForeignKey("products.Product",on_delete=models.SET_NULL,null=True,blank=True,related_name="replacement_requests")
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name="replacement_requests_created")
    decided_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="replacement_decisions")
    reason = models.CharField(max_length=30,choices=REPLACEMENT_REASON_CHOICES)
    status = models.CharField(max_length=20,choices=REQUEST_STATUS_CHOICES,default="PENDING")
    supervisor_note = models.TextField(null=True, blank=True)
    decided_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

class PickupHistory(models.Model):
    order = models.OneToOneField(Order,on_delete=models.CASCADE,related_name="pickup_history")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="customer_pickup_history")
    takeaway_staff = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="completed_pickups")
    box = models.ForeignKey("boxes.Box",on_delete=models.SET_NULL,null=True,blank=True,related_name="pickup_history")
    payment_type = models.CharField(max_length=30,null=True,blank=True)
    payment_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    qr_scanned_at = models.DateTimeField(null=True,blank=True)
    otp_verified_at = models.DateTimeField(null=True,blank=True)
    pickup_completed_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)