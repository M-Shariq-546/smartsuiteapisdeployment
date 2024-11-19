from django.db import models
from django.contrib.auth.models import AbstractUser , Group , Permission
from .managers import CustomUserManager
from django.contrib.admin import AdminSite
from phonenumber_field.modelfields import PhoneNumberField
original_get_app_list = AdminSite.get_app_list
import uuid


class CustomUser(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4 , primary_key=True,unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True , blank=True)
    username = None
    email = models.EmailField(('email address'), unique=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    cnic = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    role =models.CharField(max_length=20, choices=( ('Super Admin', 'Super Admin'), ('Teacher', 'Teacher'), ('Student', 'Student') ), default='Super Admin' )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    added_by = models.ForeignKey("self", models.CASCADE, default=None, null=True)
    is_active=models.BooleanField(default=True)
    is_deleted=models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'father_name', 'role']

    def __str__(self):
        return self.email


    class Meta:
        verbose_name = ("Super Admin")
        verbose_name_plural = ("Super Admins")

# CustomCompanyUser
class CustomDepartmentTeacher(CustomUser):
    employee_code = models.CharField(max_length=100, unique=True)
    # CustomUser.role = 'Teacher'
    class Meta:
        # proxy = True
        verbose_name = ("Department Teacher")
        verbose_name_plural = ("Department Teachers")

    def save(self, *args, **kwargs):
        self.role = 'Teacher'
        super().save(*args, **kwargs)


# CustomCompanyTeamUser
class CustomDepartmentStudent(CustomUser):
    college_roll_number = models.CharField(max_length=100, unique=True)
    university_roll_number = models.CharField(max_length=100, unique=True)
    # CustomUser.role = 'Student'
    class Meta:
        # proxy = True
        verbose_name = ("Department Student")
        verbose_name_plural = ("Department Students")

    def save(self, *args, **kwargs):
        self.role = 'Student'
        super().save(*args, **kwargs)

class MyAdminSite(AdminSite):

    def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        ordering = {
            "Super Admins": 1,
            "Department Teachers": 2,
            "Department Students": 3,
            "api":4,
            "Departments":5,
            "Courses":6,
            "Batchs":7,
            "Semesters":8,
            "Subjects":9,
            "PDFiles":10,
            "Histories":11,
            "Summaries":12,
            "Keypoints":13,
            "Quizes":14,
            "QuizResults":15,
            "Questions":16,
            "GroupChats":17,
            "Messages":18,
            "Admin_Supports":19,
            "Ticket Conversations":20,
            "Notifications":21,
            "Notifications Statuses":22,
            "Announcements":23,
        }

        app_dict = self._build_app_dict(request, app_label)

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())

        # Sort the models custom within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: ordering[x['name']])

        return app_list

AdminSite.get_app_list = MyAdminSite.get_app_list