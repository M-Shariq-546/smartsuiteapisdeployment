from rest_framework.routers import DefaultRouter
from .views import HistoryListApiView


router = DefaultRouter()


router.register(r'histories', HistoryListApiView, basename="histories")

urlpatterns = router.urls