from  rest_framework import serializers
from ..models import Semester
from .validations import *
class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'
        extra_kwargs = {
            'added_by':{'required':False},
            'name': {'required': False}
        }

    def create(self, validated_data):
        course = validated_data['course']
        batch = validated_data['batch']

        request = self.context.get("request")  # Get the request from the context
        if request is None or request.user.is_anonymous:
            raise ValidationError("Request user cannot be anonymous or None")

        validated_data['added_by'] = request.user

        for i in range(1, 9):
            semester_name = semester_name_setup(i, batch)

            Semester.objects.create(
                name = semester_name,
                course = course,
                batch = batch,
                added_by = validated_data['added_by']
            )

        response = {
            "Success":f"Successfully Created All 8 semesters for {batch}"
        }

        return response