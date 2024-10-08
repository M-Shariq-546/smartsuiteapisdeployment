from rest_framework import serializers
from ..models import Course
from departments.models import Department
from rest_framework import status
from .validations import *

class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        extra_kwargs = {
            'is_active':{'required':False},
            'created_at':{'required':False}
        }

    def create(self , validated_data):
        name = validated_data['name']
        department = validated_data['department']

        course_status = duplicate_course_check(name)

        if course_status:
            raise serializers.ValidationError({"Duplication Error":f"This Course '{name}' is already existed"})

        course = Course.objects.create(
            name = name,
            department=department
        )

        response_data = {
            "id":course.id,
            "name":course.name,
            "department":course.department.id
        }

        return response_data, course

    def update(self, instance,validated_data):
        name = validated_data['name']
        department = validated_data['department']

        if instance.name != name:
            if Course.objects.filter(name__iexact=name, is_active=True).exists():
                raise serializers.ValidationError({"Duplication Error":f"This name is already existed for course"})

        instance.name = name
        instance.save()

        response_data = {
            "id":instance.id,
            "name":instance.name,
            "department":instance.department.id,
        }

        return response_data, instance

    def delete(self, instance):
        instance.is_active=False
        instance.save()