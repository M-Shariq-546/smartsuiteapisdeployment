from .views import DepartmentModelViewSet, TeacherofDepartmentApiView
from django.urls import path , include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'department', DepartmentModelViewSet, basename='department')
router.register(r'departments', DepartmentModelViewSet, basename='departments')
urlpatterns = [
    path('', include(router.urls)),
    path('teachers_of_department/', TeacherofDepartmentApiView.as_view(), name='teachers_of_department'),
]