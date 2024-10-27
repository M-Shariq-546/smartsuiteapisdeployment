from rest_framework import serializers
from ..models import *
from django.db import transaction
from accounts.models import CustomUser

class ChatGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChat
        fields = '__all__'
        
    def validate(self, attrs):
        teacher_id = attrs.get('admin_of_group')
        
        teacher = CustomUser.objects.filter(id=teacher_id).first()
        if teacher.role != "Teacher":
            raise serializers.ValidationError({"Permission Error":"Only Teacher Could be the admin of the group"})
        
        return attrs
    
    def create(self, valiadated_data):
        students_list = valiadated_data.pop('students', [])
        
        with transaction.atomic():
            new_group_chat = GroupChat.objects.create(**valiadated_data)
            new_group_chat.students.set(students_list)
            new_group_chat.save()
        
        return new_group_chat        
        