from rest_framework import serializers
from admin_support.models import AdminSupport, TicketConversation
from django.db import transaction
from datetime import datetime

class AdminSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminSupport
        fields = '__all__'
        read_only_fields = ['submit_by']
        
    def create(self, validated_data):
        with transaction.atomic():
            new_ticket = AdminSupport.objects.create(**validated_data)    
        return new_ticket
    
class AdminSupportChatSerializer(serializers.ModelSerializer):
    ticket_status = serializers.CharField(source='ticket.ticket_status', read_only=True)
    class Meta:
        model = TicketConversation
        fields = '__all__'
        read_only_fields = ['sender']

    def create(self, validated_data):
        ticket = validated_data.get('ticket')
        user = self.context.get('request').user
        # print('=========== ticket_id ', ticket_id)
        
        if user.is_superuser:
            ticket.ticket_status = 'In-Progress'
            ticket.updated_at = datetime.now()
            ticket.save()    
                
        new_conversation = TicketConversation.objects.create(**validated_data)
        return new_conversation
    
    
class TicketResolveSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminSupport
        fields = ['ticket_status']
        
    def update(self, instance):
        instance.ticket_status = 'Resolved'
        instance.save()
        
        return instance