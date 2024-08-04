from rest_framework.routers import DefaultRouter
from .views import SemestersModelViewSets


router = DefaultRouter()

router.register("semesters", SemestersModelViewSets, basename="semesters")

urlpatterns = router.urls