from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255, help_text="Description of the action performed")
    target_content_type = models.ForeignKey(
        'contenttypes.ContentType',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        help_text="Content type of the target object (if any)"
    )
    target_object_id = models.PositiveIntegerField(null=True, blank=True, help_text="Primary key of the target object (if any)")
  
    details = models.JSONField(default=dict, blank=True, help_text="Additional details about the event, e.g., changed fields")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_email = self.user.email if self.user else "System"
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {user_email} - {self.action}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _("Audit Log Entry")
        verbose_name_plural = _("Audit Log Entries")