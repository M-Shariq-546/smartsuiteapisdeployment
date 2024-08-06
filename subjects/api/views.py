from rest_framework.viewsets import ModelViewSet
from ..models import Subjects, PDFFiles
from rest_framework.response import Response
from rest_framework import status
from history.models import History
from .serializers import *
from .permissions import *
from rest_framework.permissions import IsAuthenticated

class SubjectsModelViewSet(ModelViewSet):
    serializer_class = SubjectSerializer
    queryset = Subjects.objects.all()
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsSuperAdmin]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsSuperAdmin | IsTeacher | IsStudentForFiles]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


    def get_queryset(self):
        semester = self.request.query_params.get('semester')
        if semester:
            return Subjects.objects.filter(semester__id=semester)
        return

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        self.permission_denied(request)

    def destroy(self, request, *args, **kwargs):
        self.permission_denied(request)


class SubjectFilesModelViewSet(ModelViewSet):
    serializer_class = PDFSerializers
    permission_classes = [IsTeacherforFile | IsStudentForFiles]
    queryset = PDFFiles.objects.filter(is_active=True)

    def log_history(self, request, action, instance, changes=None):
        History.objects.create(
            user = request.user,
            action = action,
            model_name = instance.__class__.__name__,
            instance_id = instance.id,
            changes = changes,
        )

    def get_queryset(self):
        subject = self.request.query_params.get('subject')
        return PDFFiles.objects.filter(subject__id=subject, is_active=True)

    def create(self, request, *args , **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response, instance = serializer.save()
        self.log_history(request, 'CREATE', instance, f"File(s) added Successfully")
        return Response(response, status=status.HTTP_201_CREATED)


    def put(self, request, *args, **kwargs):
        kwargs['partial'] = False
        return self.update(request, *args , **kwargs)

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs['partial']
        serializer = self.get_serializer(instance , data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        self.log_history(request, 'UPDATE', instance , f"File {instance.name} updated")
        return Response(serializer.data, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_id = instance.id
        print(instance.is_active)
        instance.is_active = False
        instance.save()
        print(instance.is_active)
        print(instance_id)
        self.log_history(request, 'DELETE', instance)
        return Response({"Deleted":f"This File {instance_id} has been deleted successfully"}, status=status.HTTP_200_OK)
