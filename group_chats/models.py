from django.db import models
from accounts.models import CustomUser
import uuid

class GroupChat(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    restricted_chat = models.BooleanField(default=False)
    students = models.ManyToManyField(CustomUser, related_name='chat_studens')
    admin_of_chat = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='chat_admin')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'GroupChat'
        verbose_name_plural = 'GroupChats'
    
class Message(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    group_chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='sent_messages')
    comment = models.CharField(max_length=255, null=True, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} in {self.group_chat.name}"

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = "Messages"
