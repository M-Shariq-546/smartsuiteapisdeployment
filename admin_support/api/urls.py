from django.urls import path
from .views import *

urlpatterns = [
    path('create-ticket/', AdminSupportView.as_view(), name='create-ticket'),
    path('get-tickets/', AdminSupportView.as_view(), name='get-tickets'),
    path('get-ticket-chat/', TicketConversationView.as_view(), name='get-ticket-conversations'),
    path('create-ticket-chat/', TicketConversationView.as_view(), name='create-ticket-conversations'),
    path('resolve-ticket-chat/', ResolveTicketView.as_view(), name='resolved-ticket-conversations'),
]
