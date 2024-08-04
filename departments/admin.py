from django.contrib import admin
from .models import Department
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id' , 'name' , 'teachers' , 'is_active' , 'added_by']

    def teachers(self , obj):
        return ", ".join([str(teacher) for teacher in obj.teacher.all()])
    teachers.short_description = 'Teachers'

admin.site.register(Department , DepartmentAdmin)
