from rest_framework.viewsets import ModelViewSet
from .serializers import *
from ..models import Batch
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsSuperAdmin

class BatchModelViewSet(ModelViewSet):
    serializer_class = BatchSerializer
    permission_classes = [IsSuperAdmin]
    queryset = Batch.objects.filter(is_active=True)

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
        response_data = serializer.save()
        self.log_history(request, 'CREATE', instance, request.data)
        return Response(response_data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer()
        serializer.delete(instance)
        self.log_history(request, 'DELETE', instance)
        return Response({"Deleted SuccessFully":f"This Batch {instance.id} has been successfully deleted"}, status=status.HTTP_200_OK)
