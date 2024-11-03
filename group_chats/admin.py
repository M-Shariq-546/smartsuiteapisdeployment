from django.contrib import admin
from .models import *
@admin.register(GroupChat)
class AdminGoupChat(admin.ModelAdmin):
    list_display = ['id', 'name', 'restricted_chat', 'description', 'is_active']

@admin.register(Message)
class AdminMessages(admin.ModelAdmin):
    list_display = ['id',  'group_chat', 'comment', 'sender', 'timestamp']