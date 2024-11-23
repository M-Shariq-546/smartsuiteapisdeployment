from notifications.models import *
from subjects.api.thread import *
import threading
from rest_framework import serializers
from subjects.models import Subjects
from ..models import *
from django.db import transaction
from accounts.models import CustomUser

class studentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'name']
        
    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class ChatGroupSerializer(serializers.ModelSerializer):
    admin_of_chat = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()

    class Meta:
        model = GroupChat
        fields = '__all__'
        
    def validate(self, attrs):
        # If admin_of_chat is being updated, validate it's a Teacher
        admin_of_chat = attrs.get('admin_of_chat')
        if admin_of_chat and admin_of_chat.role != "Teacher":
            raise serializers.ValidationError({"Permission Error": "Only a Teacher can be the admin of the group"})
        
        return attrs

    def get_admin_of_chat(self, instance):
        return {
            "id": instance.admin_of_chat.id,
            "name": f"{instance.admin_of_chat.first_name} {instance.admin_of_chat.last_name}"
        }

    def get_students(self, instance):
        # Assuming studentSerializer is defined elsewhere
        return studentSerializer(instance.students.all(), many=True).data
    
    def create(self, valiadated_data):
        students_list = valiadated_data.pop('students', [])
        with transaction.atomic():
            new_group_chat = GroupChat.objects.create(**valiadated_data)
            new_group_chat.students.set(students_list)
            new_group_chat.save()
        
            threading.Thread(
                target=NotificationCreationAndSendingForMessage,
                args=("New Group Chat Created",f"Group has been created by with name {new_group_chat.name}", new_group_chat.admin_of_chat, new_group_chat)  # Pass necessary arguments to the thread
            ).start()

        return new_group_chat
        
    def get(self, instance):
        return {
                'id':instance.id,
                "name":instance.name,
                "description":instance.description,
                "restricted_chat":instance.restricted_chat,
                "admin_of_chat":{
                    "id":instance.admin_of_chat.id,
                    "name":f"{instance.admin_of_chat.first_name} {instance.admin_of_chat.last_name}"
                    },
                "students":studentSerializer(instance.students.all(), many=True),
                "created_at":instance.created_at,
                }        
        
    
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

        threading.Thread(
                target=NotificationCreationAndSendingForMessage,
                args=("Group Chat Updated","Group has been updated", instance.admin_of_chat, instance)  # Pass necessary arguments to the thread
        ).start()
        
        return {
                'id':instance.id,
                "name":instance.name,
                "description":instance.description,
                "restricted_chat":instance.restricted_chat,
                "admin_of_chat":{
                    "id":instance.admin_of_chat.id,
                    "name":f"{instance.admin_of_chat.first_name} {instance.admin_of_chat.last_name}"
                    },
                "students":studentSerializer(instance.students.all(), many=True),
                "created_at":instance.created_at,
                }
    
class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_field = ['sender']
           
    def create(self, validated_data):
        with transaction.atomic():
            new_message = Message.objects.create(**validated_data)
            threading.Thread(
                target=NotificationCreationAndSendingForMessage,
                args=("New Message",f"{new_message.comment[:15]}...", new_message.sender, new_message.group_chat)  # Pass necessary arguments to the thread
            ).start()
        return new_message
    
class StudentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'