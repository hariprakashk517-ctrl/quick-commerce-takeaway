from django.urls import path
from .views import *

urlpatterns = [
    path("all",NotificationListAPIView.as_view(),name="notification-list",),
    path("read-all/",MarkAllNotificationsReadAPIView.as_view(),name="notification-read-all",),
    path("<int:notification_id>/read/",MarkNotificationReadAPIView.as_view(),name="notification-read",),
]
