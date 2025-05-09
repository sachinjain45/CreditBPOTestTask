from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.contrib.contenttypes.models import ContentType
from .models import AuditLog
from .signals import user_registered, profile_updated, payment_successful # Import your custom signals

def get_client_ip(request):
    if not request:
        return None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def log_user_logged_in(sender, request, user, **kwargs):
    AuditLog.objects.create(
        user=user,
        action="User logged in",
        ip_address=get_client_ip(request)
    )

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    AuditLog.objects.create(
        action=f"User login failed for: {credentials.get('email', credentials.get('username', 'Unknown User'))}", # Use email or username
        ip_address=get_client_ip(request),
        details={"credentials_keys_provided": list(credentials.keys())} # Log which keys were provided, not values
    )

@receiver(user_registered)
def log_user_registered(sender, user, request, **kwargs):
    AuditLog.objects.create(
        user=user,
        action="User registered",
        ip_address=get_client_ip(request),
        target_content_type=ContentType.objects.get_for_model(user),
        target_object_id=user.pk
    )

@receiver(profile_updated)
def log_profile_updated(sender, user, profile, request, **kwargs):
    AuditLog.objects.create(
        user=user,
        action=f"{profile.__class__.__name__} updated",
        ip_address=get_client_ip(request),
        target_content_type=ContentType.objects.get_for_model(profile),
        target_object_id=profile.pk,
        details={"profile_user": profile.user.email}
    )

@receiver(payment_successful)
def log_payment_successful(sender, user, payment_record, **kwargs): # request might not be available
    AuditLog.objects.create(
        user=user,
        action="Payment successful",
        target_content_type=ContentType.objects.get_for_model(payment_record),
        target_object_id=payment_record.pk,
        details={
            "amount": str(payment_record.amount),
            "currency": payment_record.currency,
            "type": payment_record.get_payment_type_display()
        }
    )