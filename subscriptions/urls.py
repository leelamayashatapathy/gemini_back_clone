from django.urls import path
from .views import SubscribeProView, SubscriptionStatusView, StripeWebhookView

urlpatterns = [
    path('pro/', SubscribeProView.as_view(), name='subscribe-pro'),
    path('status/', SubscriptionStatusView.as_view(), name='subscription-status'),
    path('webhook/stripe/', StripeWebhookView.as_view(), name='stripe-webhook'),
] 