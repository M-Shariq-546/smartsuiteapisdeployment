from rest_framework.routers import DefaultRouter
from .views import BatchModelViewSet

router = DefaultRouter()

router.register(r'batch', BatchModelViewSet, basename="batch")

urlpatterns = router.urls
