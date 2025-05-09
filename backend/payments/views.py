from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.utils import timezone

from .models import Subscription, Payment, PaymentMethod
from .serializers import (
    SubscriptionSerializer,
    PaymentSerializer,
    PaymentMethodSerializer,
    CheckoutSessionSerializer,
)

class SubscriptionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def status(self, request):
        subscription = self.get_queryset().first()
        if not subscription:
            return Response({'tier': 'NONE'})
        return Response(self.get_serializer(subscription).data)

    @action(detail=False, methods=['post'])
    def cancel(self, request):
        subscription = self.get_queryset().first()
        if not subscription:
            return Response(
                {'error': 'No active subscription found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        subscription.cancel_at_period_end = True
        subscription.save()
        return Response({'status': 'success'})

class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def history(self, request):
        payments = self.get_queryset()
        return Response(self.get_serializer(payments, many=True).data)

    @action(detail=False, methods=['post'])
    def create_checkout_session(self, request):
        # Mock response for development
        return Response({
            'message': 'Payment functionality is disabled in this environment',
            'status': 'disabled'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

class PaymentMethodViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethod.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def update_payment_method(self, request):
        # Mock response for development
        return Response({
            'message': 'Payment functionality is disabled in this environment',
            'status': 'disabled'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)