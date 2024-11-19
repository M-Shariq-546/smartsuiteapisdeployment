from django.contrib import admin
from .models import Accouncements
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'description')

admin.site.register(Accouncements, AnnouncementAdmin)