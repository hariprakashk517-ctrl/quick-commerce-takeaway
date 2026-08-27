from django.urls import path
from .views import *

urlpatterns = [
    path('all/', CustomerOrderListAPIView.as_view(), name="customer-order-list"),
    path('create/', CreateOrderAPIView.as_view(), name="order-create"),
    path("scan-qr/", ScanQRAPIView.as_view(), name="scan-qr"),   
    path("packing/", PackingOrderListAPIView.as_view(), name="packing-order-list"),
    path("replacement-requests/",ReplacementRequestListAPIView.as_view(),name="replacement-request-list"),

    path("<str:order_id>/packing/",PackingOrderDetailAPIView.as_view(),name="packing-order-detail",),
    path("<str:order_id>/start-packing/", StartPackingAPIView.as_view(), name="start-packing"),
    path("<str:order_id>/complete-packing/", CompletePackingAPIView.as_view(), name="complete-packing"),
    path('<str:order_id>/out-for-pickup/', MarkOutForPickupAPIView.as_view(), name="mark-out-for-pickup"),
    path('<str:order_id>/refresh-pickup-credentials/',RefreshPickupCredentialsAPIView.as_view(),name="refresh-pickup-credentials"),
    path("<str:order_id>/pickup-credentials/",PickupCredentialsAPIView.as_view(),name="pickup-credentials"),
    path("<str:order_id>/verification/",OrderVerificationDetailAPIView.as_view(),name="order-verification-detail"),
    path("<str:order_id>/items/<int:item_id>/verify/",VerifyOrderItemAPIView.as_view(),name="verify-order-item"),
    path("<str:order_id>/complete-verification/",CompleteItemVerificationAPIView.as_view(),name="complete-item-verification"),
    path("<str:order_id>/items/<int:item_id>/cancel/",CancelOrderItemAPIView.as_view(),name="cancel-order-item"),
    path("<str:order_id>/items/<int:item_id>/request-replacement/",RequestReplacementAPIView.as_view(),name="request-replacement"),
    path("replacement-requests/<int:replacement_request_id>/approve/",ApproveReplacementAPIView.as_view(),name="approve-replacement"),
    path("replacement-requests/<int:replacement_request_id>/reject/",RejectReplacementAPIView.as_view(),name="reject-replacement"),
    path("replacement-requests/<int:replacement_request_id>/",ReplacementRequestDetailAPIView.as_view(),name="replacement-request-detail"),
    path("<str:order_id>/verify-otp/",VerifyPickupOTPAPIView.as_view(),name="verify-pickup-otp",),
    path("<str:order_id>/complete-pickup/",CompletePickupAPIView.as_view(),name="complete-pickup",),
    path("<str:order_id>/payment-summary/",PaymentSummaryAPIView.as_view(),name="payment-summary",),
    path("<str:order_id>/pickup-status/",PickupStatusAPIView.as_view(),name="pickup-status",),

    path('<str:order_id>/', CustomerOrderDetailAPIView.as_view(), name="customer-order-detail"),
]
