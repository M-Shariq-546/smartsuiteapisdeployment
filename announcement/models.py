from django.db import models
import uuid
from accounts.models import CustomUser


ANNOUNCEMENT_TYPES = (
    ('exams', 'exams'),
    ('holiday', 'holiday'),
    ('emergency', 'emergency'),
    ('fun-day', 'fun-day'),
    ('paper-date', 'paper-date'),
)

class Accouncements(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=255 , default='', choices=ANNOUNCEMENT_TYPES)
    announced_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='announced_by')
    to_users = models.ManyToManyField(CustomUser, related_name='to-list-accouncement')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title 
    
    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
        
    