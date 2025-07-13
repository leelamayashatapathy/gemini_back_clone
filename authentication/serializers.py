from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import OTP
from django.utils import timezone

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mobile', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            mobile=validated_data['mobile'],
            password=validated_data['password'],
            email=validated_data.get('email', None)
        )
        return user

class SendOTPSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=15)
    purpose = serializers.ChoiceField(choices=OTP.PURPOSE_CHOICES)

class VerifyOTPSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)
    purpose = serializers.ChoiceField(choices=OTP.PURPOSE_CHOICES)

class ForgotPasswordSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=15)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'mobile', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined'] 