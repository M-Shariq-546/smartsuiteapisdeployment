from rest_framework import generics 
from rest_framework import status
from rest_framework.response import Response 
from .serializers import *
from django.utils.timezone import now

from rest_framework.permissions import IsAuthenticated
from ..models import *

class NotificationsListView(generics.GenericAPIView):
    serializer_class = NotificationsListSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args , **kwargs):
        instances = Notification.objects.filter(notificationstatus__user=request.user)
        if not instances:
            return Response({'message':"No Record Found"}, status=status.HTTP_404_NOT_FOUND)    
        serializer = self.serializer_class(instances , many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class NotificationReadApiView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args , **kwargs):
        notification_id = request.GET.get('notification_id')
        notification = NotificationStatus.objects.get(notification=notification_id, user=request.user)
        notification.is_read = True
        notification.read_at = now()
        notification.save()
        return Response({'message':"success"}, status=status.HTTP_200_OK)