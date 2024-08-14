from rest_framework import serializers
from ..models import *

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
        for new_file in new_files:
            response = {
                'id':new_file.id,
                'subject':new_file.subject.name,
                'name':new_file.name,
                'file':new_file.file.url,
                'is_active':new_file.is_active
            }
            responses.append(response)
        return responses, new_file

    def update(self, instance, validated_data):
        instance.subject = validated_data.get('subject', instance.subject)
        instance.name = validated_data.get('name', instance.name)
        instance.file = validated_data.get('file', instance.file)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = '__all__'

    def create(self, validated_data):
        name= validated_data['name']
        code = validated_data['subject_code']

        if name is None or code is None:
            raise serializers.ValidationError({"Error":"subject_code or name is missings"})

        if name is not None and code is not None and Subjects.objects.filter(name =name , subject_code=code).exists():
            raise serializers.ValidationError({"Invalid Entry":f"The subject is already exists for these credentials"})

        new_subject = Subjects.objects.create(**validated_data)

        return new_subject

    def update(self, instance , validated_data):
        name = validated_data.pop('name', None)
        teacher = validated_data.pop('teacher', None)

        if teacher and name:
            instance.teacher = teacher
            instance.name = name
            instance.save()
        elif teacher is not None:
            instance.teacher = teacher
            instance.save()
        elif name is not None:
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
