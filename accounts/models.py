from django.db import models
from django.contrib.auth.models import AbstractUser
from stores.models import Store

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, unique=True, blank=False)
    full_name = models.CharField(max_length=150, blank=False)
    ROLE_CHOICES = [
        ('CUSTOMER', 'CUSTOMER'),
        ('PACKER', 'PACKER'),
        ('TAKEAWAY_STAFF', 'TAKEAWAY_STAFF'),
        ('SUPERVISOR', 'SUPERVISOR'),
        ('ADMIN', 'ADMIN'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='CUSTOMER')
    store = models.ForeignKey(Store, on_delete=models.SET_NULL,null=True,blank=True,related_name="staff_users")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class StaffRegistrationRequest(models.Model):
    ROLE_CHOICES = [
        ('PACKER', 'PACKER'),
        ('TAKEAWAY_STAFF', 'TAKEAWAY_STAFF'),
        ('SUPERVISOR', 'SUPERVISOR'),
    ]
    STATUS_CHOICES = [
        ("PENDING", "PENDING"),
        ("REJECTED", "REJECTED"),
        ("APPROVED", "APPROVED"),
    ]
    full_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150,unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10,unique=True)
    password_hash = models.CharField( max_length=255,null=True,blank=True)
    requested_role = models.CharField(max_length=50,choices=ROLE_CHOICES)
    requested_store = models.ForeignKey(Store,on_delete=models.PROTECT,related_name="staff_registration_requests")
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="PENDING")
    approved_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="approved_staff_requests")
    approved_at = models.DateTimeField(null=True,blank=True)
    rejected_reason = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - {self.requested_role} - {self.status}"
