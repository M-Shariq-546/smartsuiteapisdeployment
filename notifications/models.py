from django.db import models
import uuid
from accounts.models import CustomUser

class Notification(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    users = models.ManyToManyField(CustomUser, on_delete=models.DO_NOTHING)
    is_sent = models.BooleanField(default=True)
    sent_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"