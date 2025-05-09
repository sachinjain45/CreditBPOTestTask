from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class Role(models.TextChoices):
    SEEKER = 'SEEKER', _('Seeker')
    PROVIDER = 'PROVIDER', _('Provider')
    ADMIN = 'ADMIN', _('Admin') # For platform administrators

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', Role.ADMIN) # Superusers are Admins

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True) # Ensure email is unique
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.SEEKER
    )
    consent_given = models.BooleanField(
        _('consent to data processing'),
        default=False,
        help_text=_('Indicates if the user has consented to data processing as per PH DPA/GDPR.')
    )

    USERNAME_FIELD = 'email' # Login with email
    REQUIRED_FIELDS = ['username'] # username still required for createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.email