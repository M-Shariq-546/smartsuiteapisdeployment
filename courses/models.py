from rest_framework import serializers
from django.db import models
import uuid
from accounts.models import CustomUser
from departments.models import Department

class Course(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True , unique=True)
    name = models.CharField(max_length=300)
    department = models.ForeignKey(Department , on_delete=models.CASCADE , related_name = "Department_Courses")
    created_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ("Course")
        verbose_name_plural = ("Courses")
