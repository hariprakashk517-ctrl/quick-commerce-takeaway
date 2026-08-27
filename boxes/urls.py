from django.urls import path
from .views import *

urlpatterns = [
    path("assign/", AssignBoxAPIView.as_view(), name="assign-box"),
    path("packing-done/",PackingDoneOrdersAPIView.as_view(),name="packing-done-orders"),
    path("box-assigned/",BoxAssignedOrdersAPIView.as_view(),name="box-assigned-orders"),
]