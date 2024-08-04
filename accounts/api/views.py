from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView , DestroyAPIView , ListAPIView
from .serializers import CustomUserDetailSerializer , CustomUserSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUser
from rest_framework import status , serializers
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .permissions import IsSuperAdmin

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
                user_data = CustomUser.objects.get(email=email)
                serializer = CustomUserDetailSerializer(user_data)  # Use CustomUserDetailSerializer
                if serializer.data['role'] == 'Teacher':
                    # admin = AdminUser.objects.get(admin=serializer.data['id'])
                    
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
                        'cnic':serializer.data['cnic'],
                        'role': serializer.data['role'],
                        'created_at': serializer.data['created_at'],
                    }
                
                elif serializer.data['role'] == 'Student':
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
                        'role': serializer.data['role'],
                        'created_at': serializer.data['created_at'],
                    }
            except CustomUser.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            return JsonResponse({'token': token, 'user': serialized_user}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class TeachersListApiView(ListAPIView):
    serializer_class = CustomUserDetailSerializer
    permission_classes = [IsSuperAdmin]
    queryset = CustomUser.objects.filter(role='Teacher')

class StudentsListApiView(ListAPIView):
    serializer_class = CustomUserDetailSerializer
    permission_classes = [IsSuperAdmin]
    queryset = CustomUser.objects.filter(role='Student')

class CreateUsersApiView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    
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
        password = request.data.pop('password')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(password=make_password(password))
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
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
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance , data=request.data , partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data , status=status.HTTP_200_OK)
        
class DeleteCustomUserApiView(DestroyAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = 'id'
    
    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.role == 'Super Admin':
            pass
        return super().destroy(request, *args, **kwargs)
    