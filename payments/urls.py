from django.urls import path
from .views import *

urlpatterns = [
    path('<str:order_id>/collect/', CollectPaymentAPIView.as_view(), name="collect-payment"),
    path("<str:order_id>/cash-handover/",CashHandoverAPIView.as_view(),name="cash-handover",),
]
