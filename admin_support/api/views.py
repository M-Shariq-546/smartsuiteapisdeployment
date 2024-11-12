from rest_framework import generics  , status
from rest_framework.response import Response
from admin_support.models import AdminSupport
from .serializers import *

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
    
    
class ResolveTicketView(generics.GenericAPIView):
    serializer_class = TicketResolveSerializer
    permission_classes  = []
    
    def patch(self, request, *args , **kwargs):
        ticket_id = request.data.get('ticket_id')
        if request.user.is_superuser:
            instance = AdminSupport.objects.get(ticket_id=ticket_id)
            serializer = self.serializer_class(instance, partial=True)
            return Response({'message':f"The ticket against {ticket_id} has been resolved successfully"}, status=status.HTTP_200_OK)
        return Response({'message':"You are not authorized for this request"}, status=status.HTTP_401_UNAUTHORIZED)    