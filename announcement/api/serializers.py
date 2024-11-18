from rest_framework import serializer
from announcement.models import *
from django.db import  transaction
from accounts.models import CustomUser


class UsersListSerializer(serializer.ModelSerializer):
    name = serializer.SerializerMethodField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'name']

    def get_name(self , obj):
        return f"{obj.first_name} {obj.last_name}"

class CreateAnnouncementSerializer(serializer.ModelSerializer):
    announced_by = serializer.SerializerMethodField()
    to_list = serializer.SerialzierMethodField()
    
    class Meta:
        model = Accouncements
        fields = '__all__'
        
    def create(self, validated_data):
        with transaction.atomic():
            new_announcement = Accouncements.objects.create(**validated_data)
        return new_announcement
    
    def get_annouced_by(self, obj):
        return {'id':obj.announced_ by.id, "name":f"{obj.announced_ by.first_name} {obj.announced_ by.last_name}"}
    
    def get_to_list(self, obj):
        return UsersListSerializer(obj.to_list.all(), many=True)