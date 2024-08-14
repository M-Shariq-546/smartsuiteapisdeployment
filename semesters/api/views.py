from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from ..models import Semester
from rest_framework.response import Response
from .permissions import IsSuperAdmin
from rest_framework import status
from rest_framework import serializers

class SemestersModelViewSets(ModelViewSet):
    serializer_class = SemesterSerializer
    permission_classes = [IsSuperAdmin]
    queryset = Semester.objects.all()

    def get_queryset(self):
        course_id = self.request.query_params.get('course')
        batch_id = self.request.query_params.get('batch')

        if course_id is not None and batch_id is not None:
            return Semester.objects.filter(course__id=course_id, batch__id=batch_id)
        else:
            return []

    def create(self, request , *args , **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.save()
        return Response(response, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        kwargs['partial'] = False
        return self.update(request, *args, **kwargs)

class SemesterUpdateApiView(APIView):
    serializer_class = SemesterSerializer
    permission_classes = [IsSuperAdmin]
    def patch(self, request, id):
        instance = get_object_or_404(Semester, pk=id)
        serializer = self.serializer_class(instance , data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"Semester Updated Successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, statu=status.HTTP_400_BAD_REQUEST)
