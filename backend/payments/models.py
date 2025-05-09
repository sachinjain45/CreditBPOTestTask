from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from encrypted_model_fields.fields import EncryptedCharField, EncryptedEmailField
import uuid
import logging

logger = logging.getLogger(__name__)

class AuditLog(models.Model):
    """Model for tracking all important system events"""
    ACTION_TYPES = (
        ('CREATE', _('Create')),
        ('UPDATE', _('Update')),
        ('DELETE', _('Delete')),
        ('LOGIN', _('Login')),
        ('LOGOUT', _('Logout')),
        ('PAYMENT', _('Payment')),
        ('SUBSCRIPTION', _('Subscription')),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs'
    )
    action = models.CharField(max_length=20, choices=ACTION_TYPES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    details = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'action', 'created_at']),
            models.Index(fields=['model_name', 'object_id']),
        ]

    def __str__(self):
        return f"{self.action} by {self.user} on {self.model_name} at {self.created_at}"

class PaymentRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_records')
    stripe_charge_id = EncryptedCharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=50, default='pending')
    description = models.TextField(blank=True, null=True)
    payment_method = EncryptedCharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        
        # Create audit log
        AuditLog.objects.create(
            user=self.user,
            action='CREATE' if is_new else 'UPDATE',
            model_name='PaymentRecord',
            object_id=str(self.id),
            details={
                'amount': str(self.amount),
                'currency': self.currency,
                'status': self.status
            }
        )

    def __str__(self):
        return f"Payment {self.id} by {self.user.username if self.user else 'Unknown User'} - {self.status}"

    class Meta:
        ordering = ['-created_at']

class Subscription(models.Model):
    SUBSCRIPTION_TIERS = (
        ('NONE', _('No Subscription')),
        ('BASIC', _('Basic')),
        ('PREMIUM', _('Premium')),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscription'
    )
    tier = models.CharField(
        max_length=10,
        choices=SUBSCRIPTION_TIERS,
        default='NONE'
    )
    stripe_customer_id = EncryptedCharField(max_length=100, blank=True, null=True)
    stripe_subscription_id = EncryptedCharField(max_length=100, blank=True, null=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    cancel_at_period_end = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        old_instance = None
        if not is_new:
            old_instance = Subscription.objects.get(pk=self.pk)
        
        super().save(*args, **kwargs)
        
        # Create audit log
        AuditLog.objects.create(
            user=self.user,
            action='CREATE' if is_new else 'UPDATE',
            model_name='Subscription',
            object_id=str(self.id),
            details={
                'tier': self.tier,
                'old_tier': old_instance.tier if old_instance else None,
                'cancel_at_period_end': self.cancel_at_period_end
            }
        )

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')

    def __str__(self):
        return f"{self.user.email} - {self.tier}"

class Payment(models.Model):
    PAYMENT_STATUS = (
        ('PENDING', _('Pending')),
        ('SUCCESSFUL', _('Successful')),
        ('FAILED', _('Failed')),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='PHP')
    description = models.CharField(max_length=255)
    stripe_payment_intent_id = EncryptedCharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        old_instance = None
        if not is_new:
            old_instance = Payment.objects.get(pk=self.pk)
        
        super().save(*args, **kwargs)
        
        # Create audit log
        AuditLog.objects.create(
            user=self.user,
            action='CREATE' if is_new else 'UPDATE',
            model_name='Payment',
            object_id=str(self.id),
            details={
                'amount': str(self.amount),
                'currency': self.currency,
                'status': self.status,
                'old_status': old_instance.status if old_instance else None
            }
        )

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.amount} {self.currency}"

class PaymentMethod(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payment_methods'
    )
    stripe_payment_method_id = EncryptedCharField(max_length=100)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        
        # Create audit log
        AuditLog.objects.create(
            user=self.user,
            action='CREATE' if is_new else 'UPDATE',
            model_name='PaymentMethod',
            object_id=str(self.id),
            details={
                'is_default': self.is_default
            }
        )

    class Meta:
        verbose_name = _('Payment Method')
        verbose_name_plural = _('Payment Methods')

    def __str__(self):
        return f"{self.user.email} - {self.stripe_payment_method_id}"