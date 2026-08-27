from django.urls import path
from .views import *

urlpatterns = [
    path('all/', AddressListCreateAPIView.as_view(), name="address-list-create"),
    path("<int:pk>/", AddressDetailAPIView.as_view(), name="address-detail"),
    path("default/", DefaultAddressAPIView.as_view(), name="default-address"),
]