from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings
from .models import Subscription
from .serializers import SubscriptionStatusSerializer
from django.utils import timezone
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

stripe.api_key = settings.STRIPE_SECRET_KEY

class SubscribeProView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        user = request.user
        # Create Stripe Checkout session (sandbox)
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Gemini Pro Subscription',
                        },
                        'unit_amount': 1000,  # $10.00
                        'recurring': {'interval': 'month'},
                    },
                    'quantity': 1,
                }],
                mode='subscription',
                success_url='http://localhost:8000/success',
                cancel_url='http://localhost:8000/cancel',
                customer_email=user.email or None,
                metadata={'user_id': user.id},
            )
            return Response({'checkout_url': checkout_session.url}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SubscriptionStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            subscription = request.user.subscription
            serializer = SubscriptionStatusSerializer(subscription)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Subscription.DoesNotExist:
            return Response({'tier': 'basic', 'status': 'inactive'}, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        event = None
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # Handle event types
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            user_id = session['metadata'].get('user_id')
            stripe_subscription_id = session['subscription']
            from authentication.models import User
            try:
                user = User.objects.get(id=user_id)
                sub, created = Subscription.objects.get_or_create(user=user)
                sub.tier = 'pro'
                sub.status = 'active'
                sub.stripe_subscription_id = stripe_subscription_id
                sub.start_date = timezone.now()
                sub.save()
            except User.DoesNotExist:
                pass
        elif event['type'] == 'customer.subscription.deleted':
            subscription_obj = event['data']['object']
            stripe_subscription_id = subscription_obj['id']
            try:
                sub = Subscription.objects.get(stripe_subscription_id=stripe_subscription_id)
                sub.tier = 'basic'
                sub.status = 'inactive'
                sub.end_date = timezone.now()
                sub.save()
            except Subscription.DoesNotExist:
                pass
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
