from rest_framework import generics  , status
from rest_framework.response import Response
from admin_support.models import AdminSupport
from .serializers import *
from departments.api.permissions import IsSuperAdmin
class AdminSupportView(generics.GenericAPIView):
    serializer_class = AdminSupportSerializer
    permission_classes = []
    
    def post(self, request , *args , **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(submit_by=request.user)
            return Response({'message':f"Support Ticket Added for {request.data.get('ticket_type')} successfully"}, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args , **kwargs):
        tickets = AdminSupport.objects.filter(submit_by=request.user)
        if tickets:
            serializer = self.serializer_class(tickets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message':"No Data Found"}, status=status.HTTP_404_NOT_FOUND)
    
    
class TicketConversationView(generics.GenericAPIView):
    serializer_class = AdminSupportChatSerializer
    permission_classes = []
    
    def post(self, request, *args , **kwargs):
        serializer = self.serializer_class(data = request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(sender=request.user)
            return Response({'message':"Message Sent"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args , **kwargs):
        ticket_id = request.data.get('ticket_id')
        print(' =============== ticket id ', ticket_id)
        chats = TicketConversation.objects.filter(ticket__ticket_id=ticket_id)
        if chats:
            serializer = self.serializer_class(chats, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message':"No Data Found"}, status=status.HTTP_404_NOT_FOUND)

class UpdateTicketView(generics.GenericAPIView):
    serializer_class = AdminSupportSerializer
    permission_classes = [IsSuperAdmin]

    def patch(self, request, *args, **kwargs):
        ticket_id = request.GET.get('ticket_id')
        instance = AdminSupport.objects.get(ticket_id=ticket_id)
        instance.ticket_status = 'Resolved'
        instance.save()
        return Response({'message':f"Ticket {instance.ticket_id} has been resolved and closed successfully"}, status=status.HTTP_200_OK)