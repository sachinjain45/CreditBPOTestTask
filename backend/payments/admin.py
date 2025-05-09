# from django.contrib import admin
# from .models import PaymentRecord
#
# @admin.register(PaymentRecord)
# class PaymentRecordAdmin(admin.ModelAdmin):
#     list_display = ('user', 'stripe_charge_id', 'amount', 'currency', 'status', 'payment_type', 'created_at')
#     list_filter = ('status', 'payment_type', 'currency', 'created_at')
#     search_fields = ('user__email', 'stripe_charge_id', 'description')
#     readonly_fields = ('created_at', 'updated_at', 'stripe_charge_id') # Make stripe_charge_id readonly after creation
#     raw_id_fields = ('user',)
#
#     # Optional: Add actions, e.g., to mark a payment as refunded manually
#     # def mark_as_refunded(modeladmin, request, queryset):
#     #     queryset.update(status=PaymentRecord.PaymentStatus.REFUNDED)
#     # mark_as_refunded.short_description = "Mark selected payments as Refunded"
#     # actions = [mark_as_refunded]


# backend/payments/admin.py
from django.contrib import admin
from .models import PaymentRecord

@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_email_display', # Example custom method to display user email
        'amount',
        'currency',
        'status',
        # 'payment_type', # <--- THIS WAS THE ERROR
        'payment_method', # <--- CORRECTED to payment_method
        'created_at',
        'stripe_charge_id',
    )
    list_filter = (
        'status',
        'payment_method', # <--- CORRECTED to payment_method
        'currency',
        'created_at',
    )
    search_fields = (
        'id__iexact', # Search by exact UUID (case-insensitive for iexact, though UUIDs are usually exact)
        'user__email',
        'user__username',
        'stripe_charge_id',
        'description',
    )
    readonly_fields = ('created_at', 'updated_at', 'id', 'stripe_charge_id') # Make these read-only if appropriate
    list_per_page = 25

    # Optional: Custom method to display user's email or username in list_display
    def user_email_display(self, obj):
        return obj.user.email if obj.user else 'N/A'
    user_email_display.short_description = 'User Email' # Column header

    # If you want to make stripe_charge_id clickable to view the object
    # def view_stripe_charge_id(self, obj):
    #     return obj.stripe_charge_id
    # view_stripe_charge_id.short_description = 'Stripe/Simulated ID'

    # Ensure all fields used in list_display, list_filter, search_fields, etc.,
    # actually exist on the PaymentRecord model or are defined as methods on this admin class.