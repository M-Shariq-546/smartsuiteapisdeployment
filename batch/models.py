from django.db import models
from courses.models import Course
from accounts.models import CustomUser
import uuid
import datetime

def current_year():
    return datetime.date.today().year

def previous_years():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]


class Batch(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField(('year'), choices=previous_years , default=current_year)
    end_year = models.CharField(max_length=100, null=True , blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ManyToManyField(CustomUser, related_name='batch_students')
    is_active = models.BooleanField(default=True)
    added_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True , blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Batch"
        verbose_name_plural = "Batchs"