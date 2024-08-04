from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, CustomDepartmentStudent , CustomDepartmentTeacher 
from django import forms
import djhacker


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CompanyUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomDepartmentTeacher
        fields = '__all__'


class CompanyUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomDepartmentTeacher
        fields = '__all__'