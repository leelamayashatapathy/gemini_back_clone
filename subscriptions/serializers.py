from rest_framework import serializers
from .models import Subscription

class SubscriptionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['tier', 'status', 'start_date', 'end_date'] 