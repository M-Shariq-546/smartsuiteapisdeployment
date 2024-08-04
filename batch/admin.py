from django.contrib import admin
from .models import Batch


class BatchAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'students' , 'added_by', 'is_active']

    def students(self, obj):
        return ", ".join([str(student) for student in obj.student.all()])
    students.short_description = 'Students'

admin.site.register(Batch , BatchAdmin)
