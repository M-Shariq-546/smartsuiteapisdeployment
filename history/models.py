from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import CustomUser

user = get_user_model()


class History(models.Model):
    ACTIONS = [
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=10, choices=ACTIONS)
    timestamp = models.DateTimeField(auto_now_add=True)
    model_name = models.CharField(max_length=255)
    instance_id = models.CharField(max_length=500)
    changes = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.action} by {self.user} on {self.model_name} at {self.timestamp}"

    class Meta:
        verbose_name = "History"
        verbose_name_plural = "Histories"