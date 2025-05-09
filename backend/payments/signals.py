from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
import logging

from .models import Subscription, Payment, PaymentMethod

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Subscription)
def handle_subscription_change(sender, instance, created, **kwargs):
    """Handle subscription status changes"""
    if created:
        logger.info(f"New subscription created for user {instance.user.id}: {instance.tier}")
    else:
        logger.info(f"Subscription updated for user {instance.user.id}: {instance.tier}")

@receiver(post_save, sender=Payment)
def handle_payment_status_change(sender, instance, created, **kwargs):
    """Handle payment status changes"""
    if created:
        logger.info(f"New payment created for user {instance.user.id}: {instance.amount} {instance.currency}")
    else:
        logger.info(f"Payment status updated for user {instance.user.id}: {instance.status}")

@receiver(pre_save, sender=PaymentMethod)
def handle_payment_method_change(sender, instance, **kwargs):
    """Handle payment method changes"""
    if instance.is_default:
        # Set all other payment methods to non-default
        PaymentMethod.objects.filter(
            user=instance.user,
            is_default=True
        ).exclude(id=instance.id).update(is_default=False) 