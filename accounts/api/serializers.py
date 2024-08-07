from rest_framework import serializers
from accounts.models import CustomUser, CustomDepartmentStudent, CustomDepartmentTeacher
import datetime
from .utils import *
from threading import Thread

class CustomUserDetailSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'father_name', 'cnic', 'address', 'date_of_birth', 'age', 'email', 'phone', 'role', 'created_at']


    def get_age(self, obj):
        if obj.date_of_birth:
            today = datetime.datetime.today()
            age = today.year - obj.date_of_birth.year - (
                        (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))
            return age
        return None

class CustomUserSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'father_name', 'cnic', 'address', 'date_of_birth', 'age', 'email', 'phone', 'role', 'created_at']
        extra_kwargs = {
            'groups':{'required':False},
            'user_permissions': {'required': False},
        }

    def get_password(self , obj):
        return obj.password

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def get_age(self, obj):
        if obj.date_of_birth:
            today = datetime.datetime.today()
            age = today.year - obj.date_of_birth.year - (
                        (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))
            return age
        return None

class CustomStudentUserSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField(read_only=True)
    batch = serializers.CharField(allow_null=False, required=True, allow_blank=False)
    department = serializers.CharField(allow_null=True, required=False, allow_blank=True)
    class Meta:
        model = CustomDepartmentStudent
        fields = ['id', 'first_name', 'last_name', 'father_name', 'cnic', 'address', 'date_of_birth', 'age', 'email', 'phone', 'role', 'college_roll_number', 'university_roll_number', 'batch' , 'department', 'password', 'created_at']
        extra_kwargs = {
            'groups':{'required':False},
            'batch':{'required':False},
            'department':{'required':False},
            'user_permissions': {'required': False},
        }

    def get_password(self , obj):
        return obj.password

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A Student with this email already exists.")
        return value

    def create(self, validated_data):
        email = validated_data['email']
        new_requested_role = validated_data['role']
        password = validated_data.pop('password')
        batch_id = validated_data.pop('batch')
        department = validated_data.pop('department')
        new_student = CustomDepartmentStudent.objects.create(**validated_data)

        Thread(target=send_mail_to_new_creation, args=(email, password, new_requested_role)).start()
        Thread(target=adding_student_to_batch, args=(new_student, batch_id)).start()

        new_student.set_password(password)
        new_student.save()

        age = self.get_age(new_student)

        response = {
            'message': "Successfully Created New Student",
            'id':new_student.id,
            'first_name':new_student.first_name,
            'last_name':new_student.last_name,
            'father_name':new_student.last_name,
            'email':new_student.email,
            'phone':str(new_student.phone),
            'address':new_student.address,
            'cnic':new_student.cnic,
            'date_of_birth':new_student.date_of_birth,
            'age':age,
            'university_roll_number':new_student.university_roll_number,
            'college_roll_number':new_student.college_roll_number,
            'role':new_student.role
        }

        return response, new_student


    def get_age(self, obj):
        if obj.date_of_birth:
            today = datetime.datetime.today()
            age = today.year - obj.date_of_birth.year - (
                        (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))
            return age
        return None

class CustomTeacherUserDetailSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = CustomDepartmentTeacher
        fields = ['id', 'first_name', 'last_name', 'father_name', 'address', 'cnic', 'date_of_birth', 'age', 'email',
                  'phone', 'role', 'employee_code', 'created_at']

    def get_age(self, obj):
        if obj.date_of_birth:
            today = datetime.datetime.today()
            age = today.year - obj.date_of_birth.year - (
                        (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))
            return age
        return None


class CustomStudentUserDetailSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = CustomDepartmentStudent
        fields = ['id', 'first_name', 'last_name', 'father_name', 'address', 'cnic', 'date_of_birth', 'age', 'email',
                  'phone', 'role', 'college_roll_number', 'university_roll_number', 'created_at']

    def get_age(self, obj):
        if obj.date_of_birth:
            today = datetime.datetime.today()
            age = today.year - obj.date_of_birth.year - (
                        (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))
            return age
        return None


class CustomTeacherUserSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField(read_only=True)
    batch = serializers.CharField(allow_null=True, required=False, allow_blank=True)
    department = serializers.CharField(allow_null=False, required=True, allow_blank=False)
    class Meta:
        model = CustomDepartmentTeacher
        fields = ['id', 'first_name', 'last_name', 'father_name', 'address', 'cnic', 'date_of_birth', 'age', 'email', 'phone', 'role', 'employee_code', 'batch' , 'department', 'password', 'created_at']
        extra_kwargs = {
            'groups':{'required':False},
            'batch':{'required':False},
            'user_permissions': {'required': False},
        }

    def get_password(self , obj):
        return obj.password

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A Teacher with this email already exists.")
        return value

    def create(self, validated_data):
        department_id = validated_data.pop('department')
        email = validated_data['email']
        new_requested_role = validated_data['role']
        password = validated_data.pop('password')
        batch = validated_data.pop('batch')
        new_teacher = CustomDepartmentTeacher.objects.create(**validated_data)

        Thread(target=send_mail_to_new_creation, args=(email , new_requested_role, password)).start()
        Thread(target=adding_teacher_to_department, args=(new_teacher, department_id)).start()

        new_teacher.set_password(password)
        new_teacher.save()

        age = self.get_age(new_teacher)

        response = {
            'message':"Successfully Created New Teacher",
            'id': new_teacher.id,
            'first_name': new_teacher.first_name,
            'last_name': new_teacher.last_name,
            'father_name': new_teacher.last_name,
            'email': new_teacher.email,
            'phone': str(new_teacher.phone),
            'address': new_teacher.address,
            'cnic': new_teacher.cnic,
            'date_of_birth': new_teacher.date_of_birth,
            'age':age,
            'employee_code': new_teacher.employee_code,
            'role': new_teacher.role
        }

        return response, new_teacher

    def get_age(self, obj):
        if obj.date_of_birth:
            today = datetime.datetime.today()
            age = today.year - obj.date_of_birth.year - (
                        (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))
            return age
        return None
