from django.db import models
from semesters.models import Semester
import uuid


class Subjects(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    is_lab = models.BooleanField(default=False)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} with code {self.subject_code} belongs to {self.semester.name}"

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

class PDFFiles(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    name = models.CharField(max_length=500, null=True, blank=True)
    file = models.FileField(upload_to='files/')
    is_active= models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.file is not None and self.name is None:
            self.name = self.file.name
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "PDFile"
        verbose_name_plural = "PDFiles"