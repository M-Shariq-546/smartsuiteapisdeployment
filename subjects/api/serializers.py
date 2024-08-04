from rest_framework import serializers
from ..models import Subjects, PDFFiles

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
        return responses


    def update(self, validate_data):
        updated_files = PDFFiles.objects.update(**validated_data)
        updated_files.save()
        return updated_files

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