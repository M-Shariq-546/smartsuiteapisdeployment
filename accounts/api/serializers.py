from rest_framework import serializers
from accounts.models import CustomUser
from datetime import datetime
class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'father_name', 'cnic', 'date_of_birth', 'email', 'phone', 'role', 'created_at']


class CustomUserSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'father_name', 'cnic', 'date_of_birth', 'age', 'email', 'phone', 'role', 'created_at']
        extra_kwargs = {
            'groups':{'required':False},
            'user_permissions': {'required': False},
        }

    def get_password(self , obj):
        return obj.password

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def get_age(self, obj):
        if obj.date_of_birth:
            today = datetime.today()
            age = today.year - obj.date_of_birth.year - (
                        (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))
            return age
        return None