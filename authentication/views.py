from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model, authenticate
from .models import OTP
from .serializers import SignupSerializer, SendOTPSerializer, VerifyOTPSerializer, ForgotPasswordSerializer, ChangePasswordSerializer
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
import random

User = get_user_model()

class SignupView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendOTPView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            mobile = serializer.validated_data['mobile']
            purpose = serializer.validated_data['purpose']
            user, created = User.objects.get_or_create(mobile=mobile)
            code = str(random.randint(100000, 999999))
            expires_at = timezone.now() + timezone.timedelta(minutes=5)
            OTP.objects.create(user=user, code=code, purpose=purpose, expires_at=expires_at)
            return Response({'message': 'OTP sent', 'otp': code}, status=status.HTTP_200_OK)  # Mocked OTP
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            mobile = serializer.validated_data['mobile']
            code = serializer.validated_data['code']
            purpose = serializer.validated_data['purpose']
            try:
                user = User.objects.get(mobile=mobile)
                otp = OTP.objects.filter(user=user, code=code, purpose=purpose, is_used=False, expires_at__gte=timezone.now()).last()
                if otp:
                    otp.is_used = True
                    otp.save()
                    refresh = RefreshToken.for_user(user)
                    return Response({'message': 'OTP verified', 'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            mobile = serializer.validated_data['mobile']
            try:
                user = User.objects.get(mobile=mobile)
                code = str(random.randint(100000, 999999))
                expires_at = timezone.now() + timezone.timedelta(minutes=5)
                OTP.objects.create(user=user, code=code, purpose='forgot', expires_at=expires_at)
                return Response({'message': 'OTP sent for password reset', 'otp': code}, status=status.HTTP_200_OK)  # Mocked OTP
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            if not user.check_password(old_password):
                return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
