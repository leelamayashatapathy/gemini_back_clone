from django.urls import path
from .views import SignupView, SendOTPView, VerifyOTPView, ForgotPasswordView, ChangePasswordView, UserProfileView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
] 