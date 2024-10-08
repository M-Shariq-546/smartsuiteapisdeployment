from rest_framework import serializers
from ..models import Batch
from courses.models import Course
from courses.api.serializers import CoursesSerializer
from .validations import *
from accounts.models import CustomUser
from rest_framework.serializers import ValidationError
from semesters.models import Semester
import threading


class SuperAdminDetails(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'father_name', 'email', 'phone', 'role']

class BatchSerializer(serializers.ModelSerializer):
    students = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, required=True
    )
    class Meta:
        model = Batch
        fields = ['id', 'name', 'year', 'end_year' , 'course', 'students', 'added_by']
        read_only_fields = ['name']
        extra_kwargs = {
            "added_by":{
                'required':False
            }
        }

    def create(self, validated_data):
        year = str(validated_data['year'])
        course = validated_data['course']
        student_ids = validated_data.get('students', [])

        try:
            course = Course.objects.get(id=course.id, is_active=True)
        except Course.DoesNotExist:
            raise serializers.ValidationError({"Not Found":"Course Didn't Existed against this ID"})

        validated_data['end_year'] = str(int(year) + 4)
        name = batch_name(year, course.name, validated_data['end_year'])  # This Function is used for setting up the name of batch automatically

        check_name = validate_batch(name)
        if check_name:
            raise serializers.ValidationError({"Duplication Error":f"The Batch with name {name} is Already existed"})

        students_check , _ = students_validations(student_ids)
        if students_check:
            raise serializers.ValidationError({"Duplication Error":f"The Student {_} is already associated with any Bacth"})

        request = self.context.get("request")  # Get the request from the context
        if request is None or request.user.is_anonymous:
            raise ValidationError("Request user cannot be anonymous or None")

        validated_data['added_by'] = request.user

        new_batch = Batch.objects.create(
            name=name,
            year=year,
            end_year=validated_data['end_year'],
            course=course,
            added_by=validated_data['added_by']
        )

        threading.Thread(target=create_semesters, args=(self, new_batch.id, course.id, request.user.id)).start()
        adding_students_in_batch(new_batch, student_ids)
        students = getStudentsList(new_batch)
        response_data = {
            "name":new_batch.name,
            "course":CoursesSerializer(course).data,
            "start year":new_batch.year,
            "end year":new_batch.end_year,
            "students":students,
            "added_by":SuperAdminDetails(new_batch.added_by).data,
        }
        return response_data, new_batch

    def delete(self, instance):
        students = getStudentsList(instance)
        for student in students:
            instance.student.remove(student)
            instance.save()
        instance.is_active=False
        instance.save()
