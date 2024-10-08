from rest_framework import filters
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
from batch.models import *
from departments.models import *
from subjects.models import *
from courses.models import *
from semesters.models import *
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
                        'department':serializer.data['department'],
                        'course':serializer.data['course'],
                        'batch':serializer.data['batch'],
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
                        'created_at': serializer.data['created_at'],
                    }
            except CustomUser.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            return JsonResponse({'token': token, 'user': serialized_user}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class TeachersListApiView(ListAPIView):
    serializer_class = TeachersListSerializer
    permission_classes = [IsSuperAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['email', 'id', 'first_name', 'last_name', 'father_name', 'employee_code', 'cnic', 'date_of_birth', 'phone']
    ordering_fields = ['email', 'id', 'first_name', 'last_name', 'father_name', 'college_roll_number', 'university_roll_number', 'cnic', 'date_of_birth', 'phone']
    queryset = CustomDepartmentTeacher.objects.all()

class StudentsListApiView(ListAPIView):
    serializer_class = StudentsListSerializer
    permission_classes = [IsSuperAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['email', 'id', 'first_name', 'last_name', 'father_name', 'college_roll_number', 'university_roll_number', 'cnic', 'date_of_birth', 'phone']
    ordering_field = ['email', 'id', 'first_name', 'last_name', 'father_name', 'college_roll_number', 'university_roll_number', 'cnic', 'date_of_birth', 'phone']
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
            if serializer.is_valid(raise_exception=True):
                response , instance = serializer.save()
                self.log_history(request, "CREATE", instance, f"New Student {instance.first_name} {instance.last_name} Added Successfully")
                return Response({"message":"Teacher Created Successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif new_requested_role == 'Student':
            serializer = CustomStudentUserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                response , instance = serializer.save()
                self.log_history(request, "CREATE", instance, f"New Teacher {instance.first_name} {instance.last_name} Added Successfully")
                return Response({"message":"Student Created Successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message":"Successfully updated Student Data", "data":serializer.data} , status=status.HTTP_200_OK)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(instance, CustomDepartmentTeacher):
            partial = kwargs.pop('partial', False)
            serializer = CustomTeacherUserSerializer(instance, data=request.data, partial=partial)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message":"Successfully updated Teacher Data", "data":serializer.data}, status=status.HTTP_200_OK)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Data updated Successfully", "data": serializer.data}, status=status.HTTP_200_OK)

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
        return Response({"message":"Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)

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
        total_teachers = CustomDepartmentTeacher.objects.all().count()
        total_students = CustomDepartmentStudent.objects.all().count()
        total_departments = Department.objects.filter(is_active=True).count()
        response_data = {
            'total_teachers': total_teachers,
            'total_students': total_students,
            'total_departments':total_departments,
            'current_year': current_year_data['count'],
            'past_years': [{'year': year, 'count': data[year]} for year in past_years_range]
        }

        return Response(response_data, status=status.HTTP_200_OK)


class TeacherGetDataApiView(APIView):
    permission_classes = []
    def get(self, request):
        try:
            teacher_id = self.request.query_params.get('teacher')

            department = Department.objects.get(teacher=teacher_id)

            courses = [{"id":course.id, "course_name":course.name} for course in Course.objects.filter(department__id=department.id)]

            subjects = [{"id":subject.id, "subject_name":subject.name, 'lab':subject.is_lab} for subject in Subjects.objects.filter(teacher__id=teacher_id)]

            no_of_courses = len(courses)
            no_of_subjects_asssigned = len(subjects)
            no_of_quizes = []

            for subject in subjects:
                quiz_count = DocumentQuiz.objects.filter(document__subject__id=subject['id']).count()
                quiz_data = {
                        'subject_id':subject['id'],
                        'subject_name':subject['subject_name'],
                        'quiz_count':quiz_count
                }
                no_of_quizes.append(quiz_data)

            response = {
                'id':teacher_id,
                'department_id':department.id,
                'department_name':department.name,
                'courses':courses,
                'subjects_assigned':subjects,
                'courses_count':no_of_courses,
                'subjects_assigned_count':no_of_subjects_asssigned,
                'no_of_quizes_of_single_subject':no_of_quizes
            }

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error of {e}", status=status.HTTP_400_BAD_REQUEST)


class StudentGetDataApiView(APIView):
    permission_classes = []

    def get(self, request):
        student = self.request.query_params.get('student')

        batch = Batch.objects.get(student=student)

        semesters = [{"semester_name":semester.name, "is_active":semester.is_active} for semester in Semester.objects.filter(batch=batch.id)]

        active_semester = Semester.objects.get(batch=batch, is_active=True)

        subjects = [subject.name for subject in Subjects.objects.filter(semester__id=active_semester.id)]

        no_of_quizes_per_subeject = []

        for subject in subjects:
            quizes = [quiz for quiz in DocumentQuiz.objects.filter(document__subject__name=subject, upload=True)]

            no_of_quiz = len(quizes)

            results = []
            for quiz in quizes:
                try:
                    quiz_result = QuizResult.objects.get(quiz=quiz)
                    results.append({
                    'quiz_id': quiz_result.quiz.id,
                    'quiz_name': quiz_result.quiz.name,
                    'status': quiz_result.status,
                    'obtained_marks':quiz_result.obtained,
                    'total_marks':quiz_result.total,
                    'percentage':f"{quiz_result.score}%",
                    })
                except:
                    results.append({
                        'quiz_id': quiz.id,
                        'quiz_name': quiz.name,
                        'status': "Not Attempted",
                    })

            quiz_data = {
                'subject_name':subject,
                "quizes_count":no_of_quiz,
                'quizes_results':results
            }

            no_of_quizes_per_subeject.append(quiz_data)

        response = {
            'id':student,
            'batch_id':str(batch.id),
            'batch_name':str(batch.name),
            'course_id':str(batch.course.id),
            'course_name':str(batch.course.name),
            'current_semester':str(active_semester.name),
            'subjects':str(subjects),
            'quizes_details':no_of_quizes_per_subeject
        }

        return Response(response , status=status.HTTP_200_OK)






