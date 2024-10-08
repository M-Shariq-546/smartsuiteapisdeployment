from rest_framework.viewsets import ModelViewSet
from .serializers import CoursesSerializer
from ..models import Course
from .permissions import *
from rest_framework.response import Response
from rest_framework import status
from history.models import History
from rest_framework.permissions import IsAuthenticated

class CoursesApiView(ModelViewSet):
    serializer_class = CoursesSerializer
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.filter(is_active=True)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsSuperAdmin]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsSuperAdmin | IsTeacher]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def log_history(self, request , action , instance, changes=None):
        if changes is not None:
            changes = {k: (str(v[0]), str(v[1])) if isinstance(v[0], (str, int, float)) and isinstance(v[1], (
            str, int, float)) else str(v) for k, v in changes.items()}
        History.objects.create(
            user=request.user,
            action = action,
            model_name = instance.__class__.__name__,
            instance_id = instance.id,
            changes=changes,
        )


    #Create Courses Api View within ModelViewSet
    def get_queryset(self):
        department_id = self.request.query_params.get('department')
        if department_id:
            return Course.objects.filter(department__id=department_id, is_active=True)
        return super().get_queryset()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self , request , *args , **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response, instance = serializer.save()
            self.log_history(request, 'CREATE', instance, request.data)
            return Response({"message":"Course Created Successfully"} , status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request , *args , **kwargs):
        kwargs['partial'] = False
        return  self.update(request, *args , **kwargs)

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance , data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            changes = {}
            for field in request.data:
                if hasattr(instance, field):
                    model_value = getattr(instance, field)
                    request_value = request.data[field]
                    if model_value != request_value:
                        changes[field] = (model_value, request_value)
            response, instance = serializer.save()
            self.log_history(request, 'UPDATE', instance, changes)
            return Response({"message":"Course Updated Successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer()
        serializer.delete(instance)
        self.log_history(request, 'DELETE', instance)
        return Response({"message":f"This Course {instance.id} has been deleted successfully"}, status=status.HTTP_200_OK)