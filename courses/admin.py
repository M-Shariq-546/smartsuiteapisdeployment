from django.contrib import admin
from .models import Course

class CoursesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'department', 'is_active']
    
    
admin.site.register(Course, CoursesAdmin)
