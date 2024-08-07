from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView , DestroyAPIView , ListAPIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from accounts.models import CustomUser, CustomDepartmentTeacher, CustomDepartmentStudent
from rest_framework import status , serializers
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from batch.models import Batch
from .utils import *
from history.models import History
from django.core.mail import send_mail
from django.conf import settings
from .permissions import IsSuperAdmin
from threading import Thread

class LoginApiView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        # Authenticate user
        user = authenticate(email=email, password=password)

        if user:
            # Additional data checking (e.g., existence in DB)
            try:
                if user.role == 'Teacher':
                    user_data = CustomDepartmentTeacher.objects.get(email=email)
                    serializer = CustomTeacherUserDetailSerializer(user_data)

                    refresh = RefreshToken.for_user(user)
                    token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    }
                    serialized_user = {
                        'id': serializer.data['id'],
                        'first_name': serializer.data['first_name'],
                        'last_name': serializer.data['last_name'],
                        'father_name':serializer.data['father_name'],
                        'phone': serializer.data['phone'],
                        'email': serializer.data['email'],
                        'address':serializer.data['address'],
                        'cnic':serializer.data['cnic'],
                        'phone':serializer.data['phone'],
                        'date_of_birth':serializer.data['date_of_birth'],
                        'age':serializer.data['age'],
                        'role': serializer.data['role'],
                        'employee_code':serializer.data['employee_code'],
                        'created_at': serializer.data['created_at'],
                    }
                elif user.role == 'Student':
                    user_data = CustomDepartmentStudent.objects.get(email=email)
                    serializer = CustomStudentUserDetailSerializer(user_data)
                    refresh = RefreshToken.for_user(user)
                    token = {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                    serialized_user = {
                        'id': serializer.data['id'],
                        'first_name': serializer.data['first_name'],
                        'last_name': serializer.data['last_name'],
                        'father_name': serializer.data['father_name'],
                        'phone': serializer.data['phone'],
                        'email': serializer.data['email'],
                        'cnic': serializer.data['cnic'],
                        'address':serializer.data['address'],
                        'phone':serializer.data['phone'],
                        'date_of_birth': serializer.data['date_of_birth'],
                        'age': serializer.data['age'],
                        'role': serializer.data['role'],
                        'college_roll_number':serializer.data['college_roll_number'],
                        'university_roll_number':serializer.data['university_roll_number'],
                        'created_at': serializer.data['created_at'],
                    }
                else:
                    user_data = CustomUser.objects.get(email=email)
                    serializer = CustomUserDetailSerializer(user_data)
                    refresh = RefreshToken.for_user(user)
                    token = {
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                    }
                    serialized_user = {
                        'id': serializer.data['id'],
                        'first_name': serializer.data['first_name'],
                        'last_name': serializer.data['last_name'],
                        'father_name': serializer.data['father_name'],
                        'phone': serializer.data['phone'],
                        'email': serializer.data['email'],
                        'cnic': serializer.data['cnic'],
                        'address':serializer.data['address'],
                        'date_of_birth':serializer.data['date_of_birth'],
                        'age':serializer.data['age'],
                        'role': serializer.data['role'],
                        'total_departments':serializer.data['departments'],
                        'total_teachers':serializer.data['teachers'],
                        'total_students':serializer.data['students'],
                        'created_at': serializer.data['created_at'],
                    }
            except CustomUser.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            return JsonResponse({'token': token, 'user': serialized_user}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class TeachersListApiView(ListAPIView):
    serializer_class = CustomTeacherUserSerializer
    permission_classes = [IsSuperAdmin]
    queryset = CustomDepartmentTeacher.objects.all()

class StudentsListApiView(ListAPIView):
    serializer_class = CustomStudentUserSerializer
    permission_classes = [IsSuperAdmin]
    queryset = CustomDepartmentStudent.objects.all()

class CreateUsersApiView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
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

    def create(self, request, *args, **kwargs):
        user = self.request.user
        new_requested_role = request.data.get('role')
        
        if not user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        email = request.data.get('email')
        
        try:
            user_data = CustomUser.objects.filter(email=email).exists()
            if user_data:
                return Response({"error": f"{new_requested_role} with this email {email} already exists"}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            pass  # User does not exist, proceed with creation

        
        if user.role == 'Super Admin':
            pass  # Super Admin can create any user

        elif user.role == 'Teacher':
            new_requested_role = request.data.get('role')
            if new_requested_role != 'Student':
                return Response({"UnAuthorized": "Teacher can create Students only"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"UnAuthorized": "You do not have permission to create users."}, status=status.HTTP_401_UNAUTHORIZED)

        request.data['added_by'] = request.user.id
        if new_requested_role == 'Teacher':
            serializer = CustomTeacherUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            response , instance = serializer.save()
            self.log_history(request, "CREATE", instance, f"New Student {instance.first_name} {instance.last_name} Added Successfully")
            return Response(response, status=status.HTTP_201_CREATED)
        elif new_requested_role == 'Student':
            serializer = CustomStudentUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            response , instance = serializer.save()
            self.log_history(request, "CREATE", instance, f"New Teacher {instance.first_name} {instance.last_name} Added Successfully")
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateAccountApiView(UpdateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsSuperAdmin]
    lookup_field = 'id'
    
    def put(self, request, *args, **kwargs):
        kwargs['partial'] = False
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    
    def update(self , request , *args , **kwargs):
        instance = self.get_object()
        if isinstance(instance, CustomDepartmentStudent):
            partial = kwargs.pop('partial', False)
            serializer = CustomStudentUserSerializer(instance , data=request.data , partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        elif isinstance(instance, CustomDepartmentTeacher):
            partial = kwargs.pop('partial', False)
            serializer = CustomTeacherUserSerializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteCustomUserApiView(DestroyAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        if isinstance(instance, CustomDepartmentStudent):
            model = CustomDepartmentStudent
        elif isinstance(instance, CustomDepartmentTeacher):
            model = CustomDepartmentTeacher
        else:
            model = CustomUser

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

# This is the permission less Api for getting students and departements and teachers data
class StudentCountView(APIView):
    permission_classes = []
    def get(self, request, *args, **kwargs):
        current_year_value = current_year()
        past_years_range = [year for year, _ in previous_years() if year < current_year_value]

        # Aggregating student counts
        batch_counts = (
            Batch.objects
            .filter(year__in=past_years_range, is_active=True)
            .values('year')
            .annotate(count=Count('student'))
            .order_by('year')
        )

        # Preparing the response data
        data = {year: 0 for year in past_years_range}  # Initialize with 0 counts
        for entry in batch_counts:
            data[entry['year']] = entry['count']

        # Adding the current year count separately if not included
        current_year_data = Batch.objects.filter(year=current_year_value, is_active=True).aggregate(count=Count('student'))
        response_data = {
            'current_year': current_year_data['count'],
            'past_years': [{'year': year, 'count': data[year]} for year in past_years_range]
        }

        return Response(response_data, status=status.HTTP_200_OK)