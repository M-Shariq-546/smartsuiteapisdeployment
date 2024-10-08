# Generated by Django 5.1 on 2024-08-21 07:54

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
        ("semesters", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PDFFiles",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=500, null=True)),
                ("file", models.FileField(upload_to="files/")),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "PDFile",
                "verbose_name_plural": "PDFiles",
            },
        ),
        migrations.CreateModel(
            name="DocumentSummary",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("summary", models.TextField()),
                ("prompt", models.CharField(blank=True, max_length=500, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "added_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="summary_adder",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="document_for_summary",
                        to="subjects.pdffiles",
                    ),
                ),
            ],
            options={
                "verbose_name": "Summary",
                "verbose_name_plural": "Summaries",
            },
        ),
        migrations.CreateModel(
            name="DocumentQuiz",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("quiz", models.TextField(blank=True, null=True)),
                ("prompt", models.TextField(blank=True, max_length=500, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("upload", models.BooleanField(default=False)),
                (
                    "added_by",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quiz_added_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="subjects.pdffiles",
                    ),
                ),
            ],
            options={
                "verbose_name": "Quiz",
                "verbose_name_plural": "Quizes",
            },
        ),
        migrations.CreateModel(
            name="DocumentKeypoint",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("keypoint", models.TextField()),
                ("prompt", models.CharField(blank=True, max_length=500, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "added_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="keypoints_adder",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="keypoint",
                        to="subjects.pdffiles",
                    ),
                ),
            ],
            options={
                "verbose_name": "Keypoint",
                "verbose_name_plural": "Keypoints",
            },
        ),
        migrations.CreateModel(
            name="QuizQuestions",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("question", models.CharField(blank=True, max_length=255, null=True)),
                ("option_1", models.CharField(blank=True, max_length=255, null=True)),
                ("option_2", models.CharField(blank=True, max_length=255, null=True)),
                ("option_3", models.CharField(blank=True, max_length=255, null=True)),
                ("option_4", models.CharField(blank=True, max_length=255, null=True)),
                ("answer", models.CharField(blank=True, max_length=2, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "added_by",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quiz_question_added_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "quiz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="subjects.documentquiz",
                    ),
                ),
            ],
            options={
                "verbose_name": "Question",
                "verbose_name_plural": "Questions",
            },
        ),
        migrations.CreateModel(
            name="Subjects",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("subject_code", models.CharField(max_length=100)),
                ("description", models.CharField(max_length=500)),
                ("is_lab", models.BooleanField(default=False)),
                (
                    "semester",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="semesters.semester",
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subject_teacher",
                        to="accounts.customdepartmentteacher",
                    ),
                ),
            ],
            options={
                "verbose_name": "Subject",
                "verbose_name_plural": "Subjects",
            },
        ),
        migrations.AddField(
            model_name="pdffiles",
            name="subject",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="subjects.subjects"
            ),
        ),
        migrations.CreateModel(
            name="QuizResult",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("score", models.DecimalField(decimal_places=2, max_digits=5)),
                ("status", models.CharField(max_length=10)),
                ("obtained", models.IntegerField(blank=True, null=True)),
                ("total", models.IntegerField(blank=True, null=True)),
                (
                    "quiz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="subjects.documentquiz",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "QuizResult",
                "verbose_name_plural": "QuizResults",
                "unique_together": {("user", "quiz")},
            },
        ),
    ]
