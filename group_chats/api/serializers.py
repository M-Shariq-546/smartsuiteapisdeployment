from rest_framework import serializers
from ..models import *
from django.db import transaction
from accounts.models import CustomUser

class ChatGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChat
        fields = '__all__'
        
    def validate(self, attrs):
        # If admin_of_chat is being updated, validate it's a Teacher
        admin_of_chat = attrs.get('admin_of_chat')
        if admin_of_chat and admin_of_chat.role != "Teacher":
            raise serializers.ValidationError({"Permission Error": "Only a Teacher can be the admin of the group"})
        
        return attrs
    
    def create(self, valiadated_data):
        students_list = valiadated_data.pop('students', [])
        with transaction.atomic():
            new_group_chat = GroupChat.objects.create(**valiadated_data)
            new_group_chat.students.set(students_list)
            new_group_chat.save()
        
        return new_group_chat        
        
    def update(self, instance , validated_data):
        name = validated_data.get('name', instance.name)
        description = validated_data.get('description', instance.description)
        restricted_chat = validated_data.get('restricted_chat', instance.restricted_chat)
        students = validated_data.get('students', [])
        admin_of_chat = validated_data.get('admin_of_chat', instance.admin_of_chat)
        
        instance.name = name
        instance.description = description
        instance.restricted_chat = restricted_chat
        if admin_of_chat != instance.admin_of_chat and admin_of_chat.role != 'Teacher':
            raise serializers.ValidationError({"Permission Error": "Only a Teacher can be the admin of the group"})
        instance.admin_of_chat = admin_of_chat
        instance.save()
        
        for student in students:
            instance.students.add(student)
            instance.save()
            
        return instance
    
class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_field = ['sender']
           
    def create(self, validated_data):
        with transaction.atomic():
            new_message = Message.objects.create(**validated_data)
        return new_message