from django.urls import path
from .views import *

urlpatterns = [
    path('create-group/', CreateGroupChatView.as_view(), name='create-group'),
    path('group/', GroupGetUpdateDelete.as_view(), name='group'),
    path('groups/', CreateGroupChatView.as_view(), name='group'),
    path('send-message/', MessagesView.as_view(), name='send-message'),
    path('get-messages/', MessagesView.as_view(), name='get-messages'),
    path('select-group-members/', AddMembersApiView.as_view(), name='select-members'),
]
