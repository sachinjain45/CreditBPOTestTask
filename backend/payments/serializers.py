from rest_framework import serializers
from .models import PaymentRecord, Subscription, Payment, PaymentMethod

class PaymentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRecord
        fields = '__all__' # Or specify fields as needed for API responses

class CreateCheckoutSessionSerializer(serializers.Serializer):
    # Define fields expected from the frontend to create a checkout session
    # This depends on your product structure.
    # Example for a one-off report purchase:
    item_id = serializers.CharField(required=True, help_text="Identifier for the item being purchased (e.g., 'report_xyz')")
    # Example for subscription:
    price_id = serializers.CharField(required=False, help_text="Stripe Price ID for the subscription tier")
    # You might also pass quantity, etc.

    def validate_item_id(self, value):
        # Add validation if item_id needs to exist in your DB or match a pattern
        # For MVP, can be simple string.
        # if not MyProductModel.objects.filter(product_identifier=value).exists():
        #     raise serializers.ValidationError("Invalid item ID.")
        return value

    def validate_price_id(self, value):
        # Validate Stripe Price ID format or against known price IDs
        if value and not value.startswith('price_'):
            raise serializers.ValidationError("Invalid Stripe Price ID format.")
        return value

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'stripe_customer_id', 'stripe_subscription_id', 'tier', 'status', 'cancel_at_period_end', 'created_at', 'updated_at']
        read_only_fields = ['user', 'stripe_customer_id', 'stripe_subscription_id', 'created_at', 'updated_at']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'amount', 'currency', 'status', 'payment_method', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'user', 'stripe_payment_method_id', 'is_default', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

class CheckoutSessionSerializer(serializers.Serializer):
    price_id = serializers.CharField(required=True)
    tier = serializers.CharField(required=False)