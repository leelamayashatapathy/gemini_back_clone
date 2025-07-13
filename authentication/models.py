from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, mobile, password=None, **extra_fields):
        if not mobile:
            raise ValueError('The Mobile number must be set')
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(mobile, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    mobile = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.mobile

class OTP(models.Model):
    PURPOSE_CHOICES = (
        ('signup', 'Signup'),
        ('login', 'Login'),
        ('forgot', 'Forgot Password'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=10, choices=PURPOSE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        mobile = getattr(self.user, 'mobile', None)
        return f"OTP for {mobile or 'unknown'} - {self.purpose}"
