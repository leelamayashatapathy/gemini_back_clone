from django.db import models
from django.conf import settings

class Subscription(models.Model):
    TIER_CHOICES = (
        ('basic', 'Basic'),
        ('pro', 'Pro'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription')
    tier = models.CharField(max_length=10, choices=TIER_CHOICES, default='basic')
    stripe_subscription_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default='inactive')
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.mobile} - {self.tier}"
