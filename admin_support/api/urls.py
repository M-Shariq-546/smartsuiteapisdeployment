from django.urls import path
from .views import *

urlpatterns = [
    path('create-ticket/', AdminSupportView.as_view(), name='create-ticket'),
    path('get-tickets/', AdminSupportView.as_view(), name='get-tickets'),
    path('get-ticket-chat/', TicketConversationView.as_view(), name='get-ticket-conversations'),
    path('get-ticket-types/', TicketTypesView.as_view(), name='ticket-types'),
    path('get-ticket-id/', TicketIdView.as_view(), name='get-ticket-id'),
    path('create-ticket-chat/', TicketConversationView.as_view(), name='create-ticket-conversations'),
    path('resolve-ticket-chat/', ResolveTicketView.as_view(), name='resolved-ticket-conversations'),
]
