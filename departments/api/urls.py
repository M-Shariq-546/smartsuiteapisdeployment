from .views import DepartmentModelViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'department', DepartmentModelViewSet, basename='department')
router.register(r'departments', DepartmentModelViewSet, basename='departments')
urlpatterns = router.urls