from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'subjects', SubjectsModelViewSet, basename="crud_subjects")
router.register(r'files', SubjectFilesModelViewSet, basename='subject_files')

urlpatterns = [
    path('',include(router.urls)),
    path('summary/', CreateSummaryApiView.as_view(), name='summary'),
    path('keypoints/', CreateKeypointApiView.as_view(), name='keypoints'),
]

