from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import NotificationSerializer
from .services import NotificationService


class NotificationListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = NotificationService.list_user_notifications(request.user)

        serializer = NotificationSerializer(notifications,many=True,)

        return Response({
                "success": True,
                "message": "Notifications fetched successfully.",
                "data": serializer.data,},status=status.HTTP_200_OK,)
    
class MarkNotificationReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        notification = NotificationService.mark_notification_as_read(notification_id=notification_id,user=request.user,)

        if notification is None:
            return Response({
                    "success": False,
                    "message": "Notification not found.",
                    "data": None,
                    },status=status.HTTP_404_NOT_FOUND,)

        return Response({
                "success": True,
                "message": "Notification marked as read.",
                "data": {
                    "notification_id": notification.id,
                    "is_read": notification.is_read,
                    },},status=status.HTTP_200_OK,)
    
class MarkAllNotificationsReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        updated_count = NotificationService.mark_all_as_read(request.user)

        return Response({
                "success": True,
                "message": "All notifications marked as read.",
                "data": {
                    "updated_notifications": updated_count,
                },},status=status.HTTP_200_OK,)
    
    