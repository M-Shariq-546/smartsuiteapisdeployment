from notifications.models import *
from rest_framework import serializers

class NotificationsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'