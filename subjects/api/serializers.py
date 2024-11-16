from rest_framework import serializers
from ..models import *
import threading
from .thread import *
from accounts.models import CustomDepartmentStudent, CustomDepartmentTeacher
from notifications.models import Notification
from .thread import *
import threading

class TeacherDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomDepartmentTeacher
        fields = '__all__'
        
class StudentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class StudentsOfSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = '__all__'
        
    def get(self, instance):
        return {
            "id": instance.id,
            "name":instance.name,
            "subject_code":instance.subject_code,
            "teacher_details":TeacherDetailsSerializer(instance.teacher).data,
            "students_list":StudentDetailsSerializer(instance.semester.batch.student.all(), many=True).data,
        }


class PDFSerializers(serializers.ModelSerializer):
    class Meta:
        model = PDFFiles
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        files = self.context['request'].FILES.getlist('file')  # Get the list of files
        new_files = []
        for file in files:
            file_data = validated_data.copy()
            file_data['file'] = file
            new_file = PDFFiles.objects.create(**file_data)
            new_file.is_active = True
            new_file.save()
            new_files.append(new_file)
        responses = []
        subject_name = ''
        for new_file in new_files:
            subject_name = new_file 
            response = {
                'id':new_file.id,
                'subject':new_file.subject.name,
                'name':new_file.name,
                'file':new_file.file.url,
                'is_active':new_file.is_active
            }
            responses.append(response)
        notification_thread = threading.Thread(
                target=NotificationCreationAndSending,
                args=("New File Uploaded",f"A new file has been uploaded in {subject_name.subject.name}. Please Check it out",subject_name, self.context['request'].user)  # Pass necessary arguments to the thread
            ).start()
        return responses, new_file

    def update(self, instance, validated_data):
        file = validated_data.pop('file', None)
        name = validated_data.pop('name', None)

        if file is not None and name is not None:
            instance.file = file
            instance.name =name
            instance.save()
        elif name is not None:
            instance.name = name
            instance.save()
        elif file is not None:
            instance.file = file
            instance.save()
        else:
            raise serializers.ValidationError("File Or Name is Required")

        notification_thread = threading.Thread(
                target=NotificationCreationAndSending,
                args=("A File Updated",f"A file has been updated in {instance.subject.name}. Please Check it out",instance, self.context['request'].user)  # Pass necessary arguments to the thread
            ).start()
        
        return instance



class SubjectsOfTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields =  '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = '__all__'

    def create(self, validated_data):
        name= validated_data['name']
        code = validated_data['subject_code']

        if name is None or code is None:
            raise serializers.ValidationError({"Error":"subject_code or name is missings"})

        if name is not None and code is not None and Subjects.objects.filter(subject_code__iexact=code, is_active=True).exists():
            raise serializers.ValidationError({"Invalid Entry":f"The subject is already exists for this Code"})

        new_subject = Subjects.objects.create(**validated_data)

        return new_subject

    def update(self, instance , validated_data):
        request = self.context.get('request')
        name = validated_data.pop('name', instance.name)
        teacher = validated_data.pop('teacher', None)
        if teacher and name:
            if instance.name.lower() != name.strip().lower():
                if Subjects.objects.filter(name__iexact=name, is_active=True).exists():
                    raise serializers.ValidationError({"Invalid Entry":f"Subject with similar name 'P{name}' already exists"})
                instance.name = name
            instance.teacher = teacher
            instance.save()
            threading.Thread(target=TeacherAssignedToSubject, args=('New Teacher Added',f"Mr./Mrs. {instance.teacher.first_name} {instance.teacher.last_name} Added as New Teacher for {instance.name}" , request.user, instance)).start()
        elif teacher is not None:
            instance.teacher = teacher
            instance.save()
        elif name is not None:
            if instance.name.lower() != name.strip().lower():
                if Subjects.objects.filter(name__iexact=name, is_active=True).exists():
                    raise serializers.ValidationError({"Invalid Entry":f"Subject with similar name 'P{name}' already exists"})
            instance.name = name
            instance.save()
        else:
            raise serializers.ValidationError("Teacher id or name is required")

        return instance

class CreateQuizesSerializer(serializers.Serializer):
    class Meta:
        model = PDFFiles
        fields = ['file']


class QuizQuestionsSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    quiz = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = QuizQuestions
        fields = ['quiz', 'id', 'question', 'options', 'answer', 'created_at', 'updated_at', 'added_by']

    def get_quiz(self, obj):
        return obj.quiz.id

    def get_options(self, obj):
        return [{"A": obj.option_1, "B": obj.option_2, "C": obj.option_3, "D": obj.option_4}]


class QuizQuestionsListSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = QuizQuestions
        fields = ['quiz', 'id', 'question', 'options', 'answer']

    def get_options(self, obj):
        return [{"A": obj.option_1, "B": obj.option_2, "C": obj.option_3, "D": obj.option_4}]
