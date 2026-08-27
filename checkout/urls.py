from django.urls import path
from .views import *

urlpatterns = [
    path('all/', CheckoutAPIView.as_view(), name="checkout"),
]
