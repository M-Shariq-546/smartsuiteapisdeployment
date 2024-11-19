from rest_framework import serializers
from announcement.models import *
from django.db import  transaction
from accounts.models import CustomUser


class UsersListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'name']

    def get_name(self , obj):
        return f"{obj.first_name} {obj.last_name}"

class CreateAnnouncementSerializer(serializers.ModelSerializer):
    announced_by = serializers.SerializerMethodField(read_only=True)
    to_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Accouncements
        fields = '__all__'
        
    def create(self, validated_data):
        users = validated_data.pop('to_users')
        with transaction.atomic():
            new_announcement = Accouncements.objects.create(**validated_data)
            new_announcement.to_users.add(*users)
            new_announcement.save()
        return new_announcement
    
    def get_announced_by(self, obj):
        return {'id':obj.announced_by.id, "name":f"{obj.announced_by.first_name} {obj.announced_by.last_name}"}
    
    def get_to_list(self, obj):
        return UsersListSerializer(obj.to_users.all(), many=True).data