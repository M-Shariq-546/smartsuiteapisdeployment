from rest_framework import generics, status
from rest_framework.response import Response
from serializers import *
from .permissions import *

class CreateGroupChat(generics.GenericAPIView):
    serializer_class = ChatGroupSerializer
    permission_classes = [IsTeacherforFile]
    
    def post(self, request, *args , **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':"Group Created Successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    