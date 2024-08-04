from django.contrib import admin
from .models import Semester

class AdminSemester(admin.ModelAdmin):
    list_display = ['id', 'name', 'course', 'batch', 'added_by', 'created_at' ]

admin.site.register(Semester, AdminSemester)