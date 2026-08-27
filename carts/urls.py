from django.urls import path
from .views import *

urlpatterns = [
    path("detail/", CartDetailAPIView.as_view(), name="cart-detail"),
    path("add/", AddCartItemAPIView.as_view(), name="cart-add"),
    path("update/", UpdateCartItemAPIView.as_view(), name="cart-update"),
    path("remove/", RemoveCartItemAPIView.as_view(), name="cart-remove"),
    path("clear/", ClearCartAPIView.as_view(), name="cart-clear"),
]