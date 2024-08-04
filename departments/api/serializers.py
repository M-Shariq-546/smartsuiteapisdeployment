from rest_framework import serializers
from ..models  import Department
from accounts.models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .validations import *
class DepartmentSerializers(serializers.ModelSerializer):
    teachers = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, required=True
    )

    class Meta:
        model = Department
        fields = ['id' , 'name' , 'teachers']
        extra_kwargs = {
            'added_by':{'required':False},
        }    

    def get_teachers(self, obj):
        return [teacher.id for teacher in obj.teacher.all()]
    
    def create(self , validated_data):
        dept_name = validated_data['name']
        user = self.context['request'].user
        teacher_ids = validated_data.get('teachers' , [])

        if Department.objects.filter(name=dept_name , is_active=True).exists():
            raise serializers.ValidationError({"Duplication Error": f"Department with name {dept_name} already exists"})
                                  
        teachers = create_teachers_validations(teacher_ids)

        if teachers:
            raise serializers.ValidationError({"Duplication Error": f"Teacher(s) {teachers} are already assigned to another department"})

        with transaction.atomic():
            validated_data['added_by'] = user        
            department = Department.objects.create(
                name = dept_name,
                added_by = user 
            )
                
            # For adding each teacher
            for teacher_id in teacher_ids:
                department.teacher.add(teacher_id)
            department.save()

        teachers = self.get_teachers(department)
        response_data = {
            'id':department.id,
            'name':department.name,
            'teachers':teachers,
            'added_by':department.added_by.id
        }
        return response_data , department
            
    def update(self, instance, validated_data):
        dept_name = validated_data['name']
        new_teacher_ids = set(validated_data.get('teachers', []))
        
        if instance.name != dept_name:
            if Department.objects.filter(name=dept_name , is_active=True).exclude(id=instance.id).exists():
                raise serializers.ValidationError({"Duplication Error": f"Department with name {dept_name} already exists"})
        
        teachers , teacher_to_add , teacher_to_remove = teachers_validations(instance , new_teacher_ids)

        if teachers:
            raise serializers.ValidationError({"Duplication Error": f"Student(s) {teachers} are already part of another department"})
        
        
        with transaction.atomic():
            instance.name = dept_name
            
            for teacher_id in teacher_to_remove:
                teacher = CustomUser.objects.get(id=teacher_id)
                instance.teacher.remove(teacher)
                
            for teacher_id in teacher_to_add:
                teacher = CustomUser.objects.get(id=teacher_id)
                instance.teacher.add(teacher)

            instance.save()
        
        teachers = self.get_teachers(instance)
        response_data = {
            'id': instance.id,
            'name': instance.name,
            'teachers': teachers,
            'added_by': instance.added_by.id  
        }
        return response_data, instance
    
    def to_representation(self, instance):
        response_data = {
            'id': instance.id,
            'name': instance.name,
            'teachers': self.get_teachers(instance),
            'added_by': instance.added_by.id  # Assuming `added_by` is a `CustomUser` instance, return its ID or any other serializable field
        }
        return response_data
    
    
    def delete(self , instance):
        teachers = self.get_teachers(instance)
        for teacher_id in teachers:
            teacher = CustomUser.objects.get(id=teacher_id)
            instance.teacher.remove(teacher)
        instance.is_active = False
        instance.save()
        