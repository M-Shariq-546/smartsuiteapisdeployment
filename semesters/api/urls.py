from rest_framework.routers import DefaultRouter
from .views import SemestersModelViewSets, SemesterUpdateApiView
from django.urls import path, include

router = DefaultRouter()

router.register(r"semesters", SemestersModelViewSets, basename="semesters")

urlpatterns = [
    path('', include(router.urls)),
    path('semester/<str:id>/', SemesterUpdateApiView.as_view(), name="semester_update"),
]