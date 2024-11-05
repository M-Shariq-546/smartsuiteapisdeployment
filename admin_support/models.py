from django.db import models
import uuid
from accounts.models import CustomUser

TICKET_TYPE = (
    ('Account', 'account'),
    ('GroupChat', 'group_chat'),
    ('DownTime', 'down_time')
)

TICKET_STATUS = (
    ('Pending', 'pending'),
    ('In-Progress', 'in-progress'),
    ('Resolved', 'resolved')
)

class AdminSupport(models.Model):
    id  = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    ticket_id = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    ticket_type = models.CharField(max_length=20, default='', choices=TICKET_TYPE)
    ticket_status = models.CharField(max_length=20, default='Pending', choices=TICKET_STATUS)
    submit_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='admin_support_ticket_sender')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.ticket_id} has status {self.ticket_status}"
    
    class Meta:
        verbose_name = 'Admin_Support'
        verbose_name_plural = 'Admin_Supports'
        
        
class TicketConversation(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    message = models.CharField(max_length=255)
    ticket = models.ForeignKey(AdminSupport, on_delete=models.CASCADE, related_name='ticket_conversation')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='admin_chat')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.message[:30]
    
    class Meta:
        verbose_name = 'Ticket Conversation'
        verbose_name_plural = 'Ticket Conversations'
         