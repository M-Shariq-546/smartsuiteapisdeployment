from accounts.models import CustomUser
from ..models import Department
from rest_framework import serializers

def create_teachers_validations(teacher_ids):
    invalid = []
    for teacher_id in teacher_ids:
        teacher = CustomUser.objects.get(id=teacher_id)
        if teacher.role != 'Teacher':
            raise serializers.ValidationError({"Invalid Entry":"Please Enter the correct Teacher id"})
        if Department.objects.filter(teacher=teacher).exists():
            invalid.append(teacher_id)
                
    return invalid

def teachers_validations(instance , new_teacher_ids):        
    current_teacher_ids = set(instance.teacher.values_list('id', flat=True))
        
    teachers_to_add = new_teacher_ids - current_teacher_ids
    teachers_to_remove = current_teacher_ids - new_teacher_ids
        
    invalid = []
    for teacher_id in teachers_to_add:
        try:
            teacher = CustomUser.objects.get(id=teacher_id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"Invalid Entry": "Please enter the correct Teacher ID"})
            
        if teacher.role != 'Teacher':
            raise serializers.ValidationError({"Invalid Entry": "Please enter the correct Teacher ID"})
            
        if Department.objects.filter(teacher=teacher).exclude(id=instance.id).exists():
            invalid.append(teacher_id)
        
    return invalid , teachers_to_add , teachers_to_remove
    