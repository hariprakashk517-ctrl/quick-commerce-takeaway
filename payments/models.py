from django.db import models
from django.conf import settings

# Create your models here.
class Payment(models.Model):
    order = models.OneToOneField('orders.Order',on_delete=models.CASCADE,related_name='payment')
    PAYMENT_TYPE_CHOICES = [
        ('PREPAID', 'PREPAID'),
        ('CASH_ON_PICKUP', 'CASH_ON_PICKUP'),
        ('UPI_ON_PICKUP', 'UPI_ON_PICKUP'),
        ('CARD_ON_PICKUP', 'CARD_ON_PICKUP'),
    ]
    payment_type = models.CharField(max_length=20,choices=PAYMENT_TYPE_CHOICES,null=True,blank=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'PENDING'),
        ('PAID', 'PAID'),
        ('FAILED', 'FAILED'),
        ('REFUNDED', 'REFUNDED'),
        ('PARTIALLY_REFUNDED', 'PARTIALLY_REFUNDED'),
    ]
    status = models.CharField(max_length=20,choices=PAYMENT_STATUS_CHOICES,default='PENDING')
    transaction_id = models.CharField(max_length=100,null=True,blank=True)
    collected_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='collected_payments')
    paid_at = models.DateTimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Refund(models.Model):
    order = models.ForeignKey('orders.Order',on_delete=models.CASCADE,related_name='refunds')
    order_item = models.ForeignKey('orders.OrderItem',on_delete=models.SET_NULL,null=True,blank=True,related_name='refunds')
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    REFUND_STATUS_CHOICES = [
        ('NOT_REQUIRED', 'NOT_REQUIRED'),
        ('REFUND_IN_PROGRESS', 'REFUND_IN_PROGRESS'),
        ('REFUND_COMPLETED', 'REFUND_COMPLETED'),
        ('REFUND_FAILED', 'REFUND_FAILED'),
    ]
    status = models.CharField(max_length=30,choices=REFUND_STATUS_CHOICES,default='NOT_REQUIRED')
    reason = models.TextField(null=True,blank=True)
    processed_at = models.DateTimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CashLedger(models.Model):    
    store = models.ForeignKey('stores.Store',on_delete=models.CASCADE,related_name='cash_ledgers')
    payment = models.OneToOneField('payments.Payment',on_delete=models.CASCADE,related_name='cash_ledger')
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    collected_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='cash_collections')
    handed_over_to = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='cash_handovers_received')
    handed_over_at = models.DateTimeField(null=True,blank=True)
    CASH_LEDGER_STATUS_CHOICES = [
        ('PENDING_HANDOVER', 'PENDING_HANDOVER'),
        ('HANDED_OVER', 'HANDED_OVER'),
    ]
    status = models.CharField(max_length=30,choices=CASH_LEDGER_STATUS_CHOICES,default='PENDING_HANDOVER')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    supervisor_note = models.TextField(blank=True,null=True)
