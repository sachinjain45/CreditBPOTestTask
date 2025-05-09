from django.db import models
from django.conf import settings
from cryptography.fernet import Fernet # For django-cryptography
# from django_cryptography.fields import EncryptedCharField, EncryptedURLField # PII Encryption
from encrypted_model_fields.fields import EncryptedTextField



# Ensure CRYPTOGRAPHY_KEY is set in settings.py
# fernet = Fernet(settings.CRYPTOGRAPHY_KEY.encode()) # Not directly used here, django-cryptography handles it

class BaseProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, blank=True)
    # Location can be more structured (city, region, country) for better filtering
    location = models.CharField(max_length=255, help_text="e.g., City, Region, Country")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user.email} - {self.company_name or 'Profile'}"

class SeekerProfile(BaseProfile):
    industry = models.CharField(max_length=100, help_text="e.g., Manufacturing, Retail, Technology")
    # Encrypted PII Field example:
    rating_report_url = EncryptedTextField(
        ("Rating Report URL"),
        max_length=500,
        blank=True,
        null=True,
        help_text="Secure URL to the rating report (encrypted at rest)"
    )
    # Add other seeker-specific fields

class ProviderProfile(BaseProfile):
    # Service types could be a JSONField or a ManyToManyField to a ServiceType model
    service_types = models.JSONField(
        default=list,
        blank=True,
        help_text="List of services offered, e.g., ['Term Loan', 'Trade Finance']"
    )
    # Geoserved could also be more structured
    geos_served = models.JSONField(
        default=list,
        blank=True,
        help_text="List of geographical areas served, e.g., ['Metro Manila', 'Cebu City']"
    )
    # Subscription Tiers - can be simple CharField or ForeignKey to a SubscriptionTier model
    class SubscriptionTier(models.TextChoices):
        NONE = 'NONE', 'None'
        BASIC = 'BASIC', 'Basic'
        PREMIUM = 'PREMIUM', 'Premium'
        # Add more as needed

    subscription_tier = models.CharField(
        max_length=20,
        choices=SubscriptionTier.choices,
        default=SubscriptionTier.NONE
    )
    # Add other provider-specific fields