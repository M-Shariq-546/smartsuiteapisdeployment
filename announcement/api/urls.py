from django.urls import path
from .views import *
urlpatterns = [
    path('announcement/', AnnouncementCreateAPIView.as_view(), name='announcement-list'),
    path('announcement-types/', AnnouncementTypesView.as_view(), name='types'),
]