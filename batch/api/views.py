from rest_framework.viewsets import ModelViewSet
from .serializers import *
from ..models import Batch
from rest_framework.response import Response
from rest_framework import status
from .permissions import *
from rest_framework.permissions import IsAuthenticated


class BatchModelViewSet(ModelViewSet):
    serializer_class = BatchSerializer
    permission_classes = [IsAuthenticated]
    queryset = Batch.objects.filter(is_active=True)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsSuperAdmin]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsSuperAdmin | IsTeacher]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


    def log_history(self, request , action , instance, changes=None):
        History.objects.create(
            user=request.user,
            action = action,
            model_name = instance.__class__.__name__,
            instance_id = instance.id,
            changes=changes,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data, instance = serializer.save()
        self.log_history(request, 'CREATE', instance, request.data)
        return Response(response_data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer()
        serializer.delete(instance)
        self.log_history(request, 'DELETE', instance)
        return Response({"Deleted SuccessFully":f"This Batch {instance.id} has been successfully deleted"}, status=status.HTTP_200_OK)
