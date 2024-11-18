from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import *
from .permissions import *
from django.shortcuts import get_object_or_404

class CreateGroupChatView(generics.GenericAPIView):
    serializer_class = ChatGroupSerializer
    permission_classes = []
    
    def post(self, request, *args , **kwargs):
        if request.user.role == 'Teacher':
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'message':"Group Created Successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':"Only Teacher could create the group"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'message': "You are logged out. Please login again."}, status=status.HTTP_401_UNAUTHORIZED)
        # Filter GroupChats based on user role
        if request.user.role == 'Teacher':
            query_set = GroupChat.objects.filter(admin_of_chat=request.user, is_active=True)
        elif request.user.role == 'Student':
            query_set = GroupChat.objects.filter(students=request.user, is_active=True)
        else:
            return Response({'message': "Invalid role."}, status=status.HTTP_403_FORBIDDEN)        
        # Check if any GroupChats were found
        if query_set.exists():
            serializer = self.serializer_class(query_set, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # No GroupChats found for the user
        return Response({'message': "No Data Found"}, status=status.HTTP_404_NOT_FOUND)

class GroupGetUpdateDelete(generics.GenericAPIView):
    serializer_class = ChatGroupSerializer
    permission_classes = [] 
    
    def get(self, request, *args , **kwargs):
        if request.user.is_authenticated:
            group_id = request.GET.get('group_chat_id')
            print('============ group_id', group_id)
            instance = GroupChat.objects.filter(id=group_id, is_active=True).first()
            if instance:
                serializer = ChatGroupSerializer(instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'message':"Not Found or Group is Deleted"}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message':"You are being Logged out Please Login and Try"}, status=status.HTTP_401_UNAUTHORIZED)
        
    def patch(self, request, *args , **kwargs):
        if request.user.role == 'Teacher':
            group_id = request.GET.get('group_chat_id')
            if not group_id:
                return Response({'message':"group_chat_id is required for this request"}, status=status.HTTP_400_BAD_REQUEST)
            instance = GroupChat.objects.get(id=group_id,is_active=True)
            serializer = self.serializer_class(instance ,request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'message':"Group Updated Successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':"Only Teacher could update the group"}, status=status.HTTP_401_UNAUTHORIZED)
            
    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'Teacher':
            group_id = request.GET.get('group_chat_id')
            if not group_id:
                return Response({'message':"group_chat_id is required for this request"}, status=status.HTTP_400_BAD_REQUEST)
            instance = GroupChat.objects.get(id=group_id, is_active=True)
            instance.is_active = False
            instance.save()
            return Response({'message':f"Group === {instance.name} === deleted successfully"}, status=status.HTTP_202_ACCEPTED)
        return Response({'message':"Only Teacher could Delete the group"}, status=status.HTTP_401_UNAUTHORIZED)


class MessagesView(generics.GenericAPIView):
    serializer_class = MessagesSerializer
    permission_classes = []
    
    def post(self , request , *args , **kwargs):
        if request.user.is_authenticated:
            group_info = GroupChat.objects.filter(id=request.data.get('group_chat')).first()
            if group_info.restricted_chat:
                if request.user.role == 'Teacher':
                    serializer = self.serializer_class(data=request.data)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save(sender=request.user)
                        return Response({'message':'message sent successfully'}, status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response({'message':"Only Admin can send messages now"}, status=status.HTTP_401_UNAUTHORIZED)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(sender=request.user)
                return Response({'message':'message sent successfully'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':"You are logged out. Please login again."}, status=status.HTTP_401_UNAUTHORIZED)    
 
    def get(self, request, *args , **kwargs):
        if request.user.is_authenticated:
            group_id = request.GET.get('group_chat_id')
            query_set = Message.objects.filter(group_chat_id=group_id)
            if query_set:
                serializer = self.serializer_class(query_set, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'message': "No Data Found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message':"You are logged out. Please login again."}, status=status.HTTP_401_UNAUTHORIZED)    
 
 
class AddMembersApiView(generics.GenericAPIView):
    permission_classes = []
    
    def get(self, request, *args , **kwargs):
        try:
            if request.user.role == 'Teacher':
                subject_id = request.GET.get('subject_id')
                instance = Subjects.objects.get(id=subject_id)
                serializer = StudentDataSerializer(instance.semester.batch.student.all(), many=True)
                return Response({'message':"Data Fetched Successfully", "data":serializer.data}, status=status.HTTP_200_OK) 
            return Response({'message':"You are not authorized for this request"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'message':f"{e}"}, status=status.HTTP_400_BAD_REQUEST)