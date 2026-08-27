from django.db import models
from django.conf import settings

class Address(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ('HOME', 'HOME'),
        ('WORK', 'WORK'),
        ('OTHER', 'OTHER'),
    ]
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='addresses')
    address_type = models.CharField(max_length=20,choices=ADDRESS_TYPE_CHOICES,default='HOME')
    full_address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_default = models.BooleanField(default=False)
    last_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    selected_store = models.ForeignKey('stores.Store',on_delete=models.SET_NULL,null=True,blank=True,related_name='selected_addresses')
    distance_from_store_km = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)