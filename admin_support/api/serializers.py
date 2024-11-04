from rest_framework import serializers
from admin_support.models import AdminSupport, TicketConversation
from django.db import transaction

class AdminSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminSupport
        fields = '__all__'
        
    def create(self, validated_data):
        with transaction.atomic():
            new_ticket = AdminSupport.objects.create(**validated_data)    
        return new_ticket
    
class AdminSupportChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketConversation
        fields = '__all__'
        
    def create(self, validated_data):
        ticket_id = validated_data.get('ticket_id')
        user = self.context.get('request').user
        
        if user.is_superuser:
            AdminSupport.objects.get(ticket_id=ticket_id).update(ticket_status='In-Progress')
        
        
        return None