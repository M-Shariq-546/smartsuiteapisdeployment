from django.db import models
import uuid
from accounts.models import CustomUser

NOTIFICATION_TYPES = (
    ('file', 'file'),
    ('chat', 'chat'),
    ('summary', 'summary'),
    ('keypoint', 'keypoint'),
    ('quiz', 'quiz')
)

class Notification(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)  # Optional description
    type = models.CharField(max_length=255, choices=NOTIFICATION_TYPES, default='file')  # Corrected field name
    users = models.ManyToManyField(
        CustomUser,
        through='NotificationStatus',  # Intermediary model
        related_name='notifications'
    )
    is_sent = models.BooleanField(default=False)  # Default set to False for logical initialization
    sent_by = models.ForeignKey(
        CustomUser,
        on_delete=models.DO_NOTHING,
        related_name='notifications_sent'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

class NotificationStatus(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)  # Tracks if the user has read the notification
    read_at = models.DateTimeField(null=True, blank=True)  # Timestamp for when the notification was read

    class Meta:
        unique_together = ('user', 'notification')
        verbose_name = "Notification Status"
        verbose_name_plural = "Notifications Statuses"
