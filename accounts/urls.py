from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('token/',TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path("register/staff/",StaffRegistrationAPIView.as_view(),name="staff-register"),
    path("staff-requests/",StaffRegistrationRequestListAPIView.as_view(),name="staff-registration-requests",),
    path("staff-requests/<int:request_id>/approve/",StaffRegistrationApprovalAPIView.as_view(),name="approve-staff-registration",),
]
