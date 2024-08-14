from django.db import models
from courses.models import Course
from batch.models import Batch
from accounts.models import CustomUser
import uuid

class Semester(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    added_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Semester"
        verbose_name_plural = "Semesters"


# This is testing and checking push

