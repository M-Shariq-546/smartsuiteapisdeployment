from rest_framework.response import Response
from announcement.models import Accouncements
from .serializers import *
from rest_framework import generics, status

class AnnouncementCreateAPIView(generics.CreateAPIView):
    serializer_class = CreateAnnouncementSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(announced_by=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        instances = Accouncements.objects.all()
        if instances:
            serializer = self.get_serializer(instances, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message':"No Record Found"},status=status.HTTP_404_NOT_FOUND)