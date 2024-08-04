from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin
from .models import CustomUser, CustomDepartmentTeacher , CustomDepartmentStudent
from .forms import CustomUserCreationForm, CustomUserChangeForm, CompanyUserCreationForm, CompanyUserChangeForm
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from django.utils import timezone, dateformat
# from documents.models import DocumentTeam, UserDocuments


def day_hour_format_converter(date_time_UTC):
    return dateformat.format(
        timezone.localtime(date_time_UTC),
        'm/d/Y H:i:s',
    )

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    model = CustomUser
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_active', 'role', 'created','updated','added_by')
    list_filter = ('is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', ('first_name', 'last_name'))}),
        ('Permissions', {'fields' : ('is_active',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', ('first_name', 'last_name'))}
        ),
        ('Permissions', {'fields' : ('is_active',)}),
    )
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('-id',)

    def updated(self, obj):
        if obj.updated_at:
            return day_hour_format_converter(obj.updated_at)
    updated.short_description = 'UPDATED AT' 

    def created(self, obj):
        if obj.created_at:
            return day_hour_format_converter(obj.created_at)
    created.short_description = 'CREATED AT' 

 
    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        if obj.role == 'Super Admin':
            obj.is_staff = True
            obj.is_superuser = True
        else:
            obj.is_staff = True
            obj.is_superuser = False
            
        if obj.id is None:
            obj.added_by = request.user
        elif obj.added_by is None:    
            obj.added_by = request.user

        obj.save()

        permissions = Permission.objects.filter(pk__in =(28,32,36,40,44))
        obj.user_permissions.add(*permissions)
 
    # default backend filter for list display
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=True)
    
 
class CustomDepartmentTeacherAdmin(UserAdmin):
    add_form = CompanyUserCreationForm
    form = CompanyUserChangeForm

    model = CustomDepartmentTeacher
    list_display = ('id','email', 'first_name', 'last_name', 'is_active', 'role', 'created','updated','added_by')
    list_filter = ('is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', ('first_name', 'last_name'))}),
        ('Permissions', {'fields' : ('is_active',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', ('first_name', 'last_name'))}
        ),
        ('Permissions', {'fields' : ('is_active',)}),
    )
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('-id',)

    def updated(self, obj):
        if obj.updated_at:
            return day_hour_format_converter(obj.updated_at)
    updated.short_description = 'UPDATED AT' 

    def created(self, obj):
        if obj.created_at:
            return day_hour_format_converter(obj.created_at)
    created.short_description = 'CREATED AT' 


    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        
        obj.is_staff = True
        obj.is_superuser = False
        obj.role = 'Teacher'

        if obj.id is None:
            obj.added_by = request.user
        elif obj.added_by is None:    
            obj.added_by = request.user

        obj.save()

        permissions = Permission.objects.filter(pk__in =(28,32,36,40,44))
        obj.user_permissions.add(*permissions)
        
    # default backend filter for list display
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=False, role='Teacher')


class CustomDepartmentStudentAdmin(UserAdmin):
    add_form = CompanyUserCreationForm
    form = CompanyUserChangeForm

    model = CustomDepartmentStudent
    list_display = ('id','email', 'first_name', 'last_name', 'is_active', 'role', 'created','updated','added_by')
    list_filter = ('is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', ('first_name', 'last_name'))}),
        ('Permissions', {'fields' : ('is_active',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', ('first_name', 'last_name'))}
        ),
        ('Permissions', {'fields' : ('is_active',)}),
    )
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('-id',)

    def updated(self, obj):
        if obj.updated_at:
            return day_hour_format_converter(obj.updated_at)
    updated.short_description = 'UPDATED AT' 

    def created(self, obj):
        if obj.created_at:
            return day_hour_format_converter(obj.created_at)
    created.short_description = 'CREATED AT' 


    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        
        obj.is_staff = True
        obj.is_superuser = False
        obj.role = 'Student'

        if obj.id is None:
            obj.added_by = request.user
        elif obj.added_by is None:    
            obj.added_by = request.user

        obj.save()

        permissions = Permission.objects.filter(pk__in =(28,32,36,40,44))
        obj.user_permissions.add(*permissions)
        
    # default backend filter for list display
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=False, role='Student')


            
admin.site.register(CustomUser, CustomUserAdmin,)
admin.site.unregister(Group)
admin.site.register(CustomDepartmentTeacher, CustomDepartmentTeacherAdmin)
admin.site.register(CustomDepartmentStudent, CustomDepartmentStudentAdmin)
