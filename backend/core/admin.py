from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user_display', 'action', 'ip_address', 'target_object_display')
    list_filter = ('timestamp', 'user', 'action') # Add target_content_type if useful
    search_fields = ('user__email', 'action', 'details', 'ip_address')
    readonly_fields = ('timestamp', 'user', 'action', 'ip_address', 'details', 'target_content_type', 'target_object_id') # Make all readonly

    def user_display(self, obj):
        return obj.user.email if obj.user else "System"
    user_display.short_description = "User"

    def target_object_display(self, obj):
        if obj.target_content_type and obj.target_object_id:
            try:
                target_model = obj.target_content_type.model_class()
                target_instance = target_model.objects.get(pk=obj.target_object_id)
                return f"{obj.target_content_type.model.capitalize()}: {str(target_instance)[:50]}"
            except Exception:
                return f"{obj.target_content_type.model.capitalize()} ID: {obj.target_object_id} (Instance not found or error)"
        return "-"
    target_object_display.short_description = "Target Object"