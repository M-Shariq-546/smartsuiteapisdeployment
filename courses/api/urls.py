from rest_framework.routers import DefaultRouter
from .views import CoursesApiView

router = DefaultRouter()
router.register(r'courses', CoursesApiView, basename='courses')
router.register(r'course', CoursesApiView, basename='course')
urlpatterns = router.urls