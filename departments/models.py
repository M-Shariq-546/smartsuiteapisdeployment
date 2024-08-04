from django.db import models
from accounts.models import CustomUser , CustomDepartmentStudent , CustomDepartmentTeacher
import uuid

class Department(models.Model):
    id = models.UUIDField(default=uuid.uuid4 , primary_key=True , unique=True)
    name = models.CharField(max_length=200)
    teacher = models.ManyToManyField(CustomUser,related_name="Department_Teacher")
    added_by = models.ForeignKey(CustomUser , on_delete=models.CASCADE,related_name="Department_Adder")
    is_active= models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = ('Department')
        verbose_name_plural = ('Departments')
    
