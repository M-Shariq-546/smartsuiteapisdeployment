from accounts.models import CustomUser, CustomDepartmentTeacher
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
    teacher = models.ForeignKey(CustomDepartmentTeacher, on_delete=models.CASCADE, null=True, blank=True, related_name='subject_teacher')

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
    prompt = models.CharField(max_length=500,blank=True, null=True)
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
    prompt = models.CharField(max_length=500,blank=True, null=True)
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
    name = models.CharField(max_length=255)
    quiz = models.TextField(blank=True, null=True)
    prompt = models.TextField(max_length=500,blank=True, null=True)
    document = models.ForeignKey(PDFFiles, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    upload = models.BooleanField(default=False)
    added_by = models.ForeignKey(CustomUser, models.CASCADE, default=None, null=True, related_name="quiz_added_by")

    def __str__(self):
        return self.name

    def delete_quiz(self):
        self.delete()

    class Meta:
        verbose_name = ("Quiz")
        verbose_name_plural = ("Quizes")


class QuizQuestions(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    question = models.CharField(max_length=255, blank=True, null=True)
    option_1 = models.CharField(max_length=255, blank=True, null=True)
    option_2 = models.CharField(max_length=255, blank=True, null=True)
    option_3 = models.CharField(max_length=255, blank=True, null=True)
    option_4 = models.CharField(max_length=255, blank=True, null=True)
    answer = models.CharField(max_length=2, blank=True, null=True)
    quiz = models.ForeignKey(DocumentQuiz, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    added_by = models.ForeignKey(CustomUser, models.CASCADE, default=None, null=True,
                                 related_name="quiz_question_added_by")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = ("Question")
        verbose_name_plural = ("Questions")


class QuizResult(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(DocumentQuiz, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=10)
    obtained = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)
    class Meta:
        unique_together = ('user', 'quiz')

        verbose_name = "QuizResult"
        verbose_name_plural = "QuizResults"
    def __str__(self):
        return f"{self.user.first_name} - {self.quiz.name} - {self.status}"
