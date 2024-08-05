from rest_framework.viewsets import ModelViewSet
from ..models import Department
from .permissions import *
from .serializers import DepartmentSerializers, TeachersofDepartment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from history.models import History
from accounts.models import CustomUser
from rest_framework.permissions import IsAuthenticated
class DepartmentModelViewSet(ModelViewSet):
    serializer_class = DepartmentSerializers
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.filter(is_active=True)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsSuperAdmin]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsSuperAdmin | IsTeacher]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


    def log_history(self, request , action , instance, changes=None):
        field_mapping = {
            'teachers': 'teacher',  # Example mapping, add more if necessary
        }

        changes = {}
        for request_field, model_field in field_mapping.items():
            if request_field in request.data:
                model_value = list(getattr(instance, model_field).values_list('id',
                                                                              flat=True)) if request_field == 'teachers' else getattr(
                    instance, model_field)
                request_value = request.data[request_field]
                if model_value != request_value:
                    changes[model_field] = (model_value, request_value)

        History.objects.create(
            user=request.user,
            action = action,
            model_name = instance.__class__.__name__,
            instance_id = instance.id,
            changes=changes,
        )

    def get_queryset(self):
        teacher_id = self.request.query_params.get('teacher')
        if teacher_id:
            return Department.objects.filter(teacher__id=teacher_id, is_active=True)
        return super().get_queryset()    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data, instance = serializer.save()
        # self.log_history(request, 'CREATE', instance, "Department created")
        return Response(response_data, status=status.HTTP_200_OK)
    
    
    def put(self , request , *args , **kwargs):
        kwargs['partial'] = False
        return self.update(request , *args , **kwargs)
    
    def patch(self , request , *args , **kwargs):
        kwargs['partial'] = True
        return self.update(request , *args , **kwargs)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data , partial=partial)
        serializer.is_valid(raise_exception=True)
        response_data, instance = serializer.save()
        # self.log_history(request, 'UPDATE', instance, request.data)
        return Response(response_data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        response = self.get_serializer(instance)
        return Response(response.data , status=status.HTTP_200_OK)
            
    def destroy(self , request , *args , **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer()
        serializer.delete(instance)
        # self.log_history(request, 'DELETE', instance)
        return Response({"Success Message":f"Department with id {instance.id} has been deleted successfully"} , status=status.HTTP_200_OK)


class TeacherofDepartmentApiView(APIView):
    serializer_class = TeachersofDepartment
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsSuperAdmin]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsSuperAdmin | IsTeacher]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


    def get(self, request, *args, **kwargs):
        department_id = request.query_params.get('department')
        if not department_id:
            return Response({"error": "Department ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            return Response({"error": "Department not found."}, status=status.HTTP_404_NOT_FOUND)

        teachers = department.teacher.all()
        serializer = self.serializer_class(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
