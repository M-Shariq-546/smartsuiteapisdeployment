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