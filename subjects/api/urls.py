from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'subjects', SubjectsModelViewSet, basename="crud_subjects")
router.register(r'files', SubjectFilesModelViewSet, basename='subject_files')


urlpatterns = [
    path('',include(router.urls)),
    path('subjects_of_teacher/', SubjectsOfTeacher.as_view(), name='subjects_of_teachers'),
    path('subject_delete/<str:id>/', SubjectDeleteAPIView.as_view(), name='subject_delete'),
    path('file/<str:id>/', FileUpdteApiView.as_view(), name='file_update'),
    path('subject_detail/<str:id>/', SubjectDetailAPIView.as_view(), name='subject_detail'),
    path('subject_update/<str:id>/', AssignTeacherToSubject.as_view(), name='assign_teacher_to_subject'),
    path('summary/', CreateSummaryApiView.as_view(), name='summary'),
    path('keypoints/', CreateKeypointApiView.as_view(), name='keypoints'),
    path('quiz/upload/', UploadQuiz.as_view(), name="uploadQuiz"),
    path('question/<uuid:question_id>/', EditQuizes.as_view(), name="EditQuestion"),
    path('quiz/', CreateQuizessApiView.as_view(), name='create-quiz'),
    path('quiz/submit/', SubmitQuizView.as_view(), name='submit_quiz'),
    path('students_of_subjects/', StudentsOfSubjectsView.as_view(), name='student_of_subject'),
    path('questions/', QuestionsofQuiz.as_view(), name='questions-of-quiz'),
    path("quiz/<str:quiz_id>/", CreateQuizessApiView.as_view(), name='delete_quiz'),
]

