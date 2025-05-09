from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import SeekerProfile, ProviderProfile
from users.models import Role # Assuming User model is in users.models

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == Role.SEEKER:
            SeekerProfile.objects.create(user=instance)
        elif instance.role == Role.PROVIDER:
            ProviderProfile.objects.create(user=instance)
        # Admin users might not need a specific profile, or you can define one

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    # In case the role changes, you might want to handle profile creation/deletion here too
    # For simplicity, this example assumes role is set at creation and doesn't change
    # or if it changes, profiles are managed manually or by another process.
    try:
        if instance.role == Role.SEEKER and hasattr(instance, 'seekerprofile'):
            instance.seekerprofile.save()
        elif instance.role == Role.PROVIDER and hasattr(instance, 'providerprofile'):
            instance.providerprofile.save()
    except (SeekerProfile.DoesNotExist, ProviderProfile.DoesNotExist):
        # If profile was deleted manually and user saved again, recreate it
        if instance.role == Role.SEEKER:
            SeekerProfile.objects.get_or_create(user=instance)
        elif instance.role == Role.PROVIDER:
            ProviderProfile.objects.get_or_create(user=instance)