from accounts.models import CustomUser
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


class DocumentSummary(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    summary = models.TextField()
    prompt = models.CharField(blank=True, null=True)
    document = models.ForeignKey(PDFFiles, on_delete=models.CASCADE, related_name='document_for_summary')
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='summary_adder')

    def __str__(self):
        return self.document.name

    class Meta:
        verbose_name = "Summary"
        verbose_name_plural = "Summaries"


class DocumentKeypoint(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    keypoint = models.TextField()
    prompt = models.CharField(blank=True, null=True)
    document = models.ForeignKey(PDFFiles, on_delete=models.CASCADE, related_name='keypoint')
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='keypoints_adder')

    def __str__(self):
        return self.document.name

    class Meta:
        verbose_name = "Keypoint"
        verbose_name_plural = "Keypoints"


class DocumentQuiz(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    name = models.TextField(max_length=255)
    quiz = models.TextField(max_length=255)
    document = models.ForeignKey(PDFFiles, on_delete=models.CASCADE, related_name='document_for_quiz')
    upload = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="quiz")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizes"