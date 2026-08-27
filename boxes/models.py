from django.db import models

# Create your models here.
from django.db import models


class Box(models.Model):
    box_id = models.CharField(max_length=10,unique=True)
    store = models.ForeignKey('stores.Store',on_delete=models.CASCADE,related_name='boxes')
    BOX_STATUS_CHOICES = [
        ('AVAILABLE', 'AVAILABLE'),
        ('OCCUPIED', 'OCCUPIED'),
    ]
    status = models.CharField(max_length=20,choices=BOX_STATUS_CHOICES,default='AVAILABLE')
    assigned_order = models.OneToOneField('orders.Order',on_delete=models.SET_NULL,null=True,blank=True,related_name='box')
    assigned_at = models.DateTimeField(null=True,blank=True)
    released_at = models.DateTimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)