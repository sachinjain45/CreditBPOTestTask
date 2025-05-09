from django.contrib import admin
from .models import SeekerProfile, ProviderProfile

@admin.register(SeekerProfile)
class SeekerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'industry', 'location', 'rating_report_url', 'updated_at')
    search_fields = ('user__email', 'company_name', 'industry', 'location')
    list_filter = ('industry', 'location')
    raw_id_fields = ('user',) # For better performance with many users

@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'subscription_tier', 'location', 'updated_at')
    search_fields = ('user__email', 'company_name', 'location')
    list_filter = ('subscription_tier', 'location')
    raw_id_fields = ('user',)