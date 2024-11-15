from django.urls import path
from .views import *

urlpatterns = [
    path('notifications/', NotificationsListView.as_view(), name='notifications-list'),
    path('read-notification/', NotificationReadApiView.as_view(), name='read-notification')
]
