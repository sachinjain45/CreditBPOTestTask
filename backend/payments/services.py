# import stripe
# from django.conf import settings
# from .models import PaymentRecord
# from profiles.models import ProviderProfile # To update subscription tier
# from users.models import User # To associate payment with user
# from core.signals import payment_successful # For audit log and notifications
#
# stripe.api_key = settings.STRIPE_SECRET_KEY
#
# def create_stripe_checkout_session(user: User, item_type: str, item_id: str = None, price_id: str = None, quantity: int = 1):
#     """
#     Creates a Stripe Checkout session.
#     item_type: 'report' or 'subscription'
#     item_id: Your internal ID for a report (used to lookup Stripe Price ID or define line item)
#     price_id: Stripe Price ID for subscription
#     """
#     success_url = f"{settings.SITE_URL}/payment/success?session_id={{CHECKOUT_SESSION_ID}}"
#     cancel_url = f"{settings.SITE_URL}/payment/cancel"
#
#     line_items = []
#     mode = 'payment' # Default for one-off
#
#     if item_type == 'report':
#         # You'd typically look up the Stripe Price ID based on your item_id
#         # or define the product ad-hoc if it's dynamic.
#         # For MVP, let's assume a fixed price ID for "report purchase"
#         if not settings.STRIPE_REPORT_PRICE_ID:
#             raise ValueError("STRIPE_REPORT_PRICE_ID not configured in settings.")
#         line_items.append({
#             'price': settings.STRIPE_REPORT_PRICE_ID,
#             'quantity': quantity,
#         })
#     elif item_type == 'subscription':
#         if not price_id: # price_id should be passed for subscriptions
#             raise ValueError("Stripe Price ID is required for subscriptions.")
#         line_items.append({
#             'price': price_id,
#             'quantity': quantity, # Usually 1 for subscriptions
#         })
#         mode = 'subscription'
#     else:
#         raise ValueError(f"Unsupported item_type: {item_type}")
#
#     try:
#         checkout_session = stripe.checkout.Session.create(
#             client_reference_id=str(user.id), # Link session to your user ID
#             customer_email=user.email, # Pre-fill email
#             payment_method_types=['card'],
#             line_items=line_items,
#             mode=mode,
#             success_url=success_url,
#             cancel_url=cancel_url,
#             # For subscriptions, you might want to allow promotion codes
#             # allow_promotion_codes=True,
#             # Metadata can be useful to store extra info that comes back in webhooks
#             metadata={
#                 'user_id': str(user.id),
#                 'item_type': item_type,
#                 'item_id': item_id or price_id, # Store relevant ID
#             }
#         )
#         return checkout_session
#     except stripe.error.StripeError as e:
#         # Handle Stripe errors (log them, return specific error to user)
#         print(f"Stripe error creating checkout session: {e}")
#         raise
#
#
# def handle_checkout_session_completed(session):
#     """
#     Handles the 'checkout.session.completed' webhook event.
#     """
#     print(f"Checkout session completed: {session.id}")
#     user_id = session.get('client_reference_id') or session.get('metadata', {}).get('user_id')
#     payment_intent_id = session.get('payment_intent')
#     subscription_id = session.get('subscription') # For subscriptions
#     item_type = session.get('metadata', {}).get('item_type', 'UNKNOWN')
#     item_id = session.get('metadata', {}).get('item_id', 'UNKNOWN')
#
#     if not user_id:
#         print(f"Error: User ID not found in checkout session {session.id}")
#         return
#
#     try:
#         user = User.objects.get(id=user_id)
#     except User.DoesNotExist:
#         print(f"Error: User with ID {user_id} not found for session {session.id}")
#         return
#
#     # Ensure payment isn't processed twice
#     if PaymentRecord.objects.filter(stripe_charge_id=session.id).exists():
#         print(f"Webhook for session {session.id} already processed.")
#         return
#
#     payment_record = PaymentRecord.objects.create(
#         user=user,
#         stripe_charge_id=session.id, # Use session ID as a reference until payment_intent is confirmed
#         amount=session.amount_total / 100.0, # Amount is in cents
#         currency=session.currency.upper(),
#         status=PaymentRecord.PaymentStatus.PENDING, # Initially pending, will be updated by payment_intent.succeeded
#         payment_type=PaymentRecord.PaymentType.REPORT_PURCHASE if item_type == 'report' else PaymentRecord.PaymentType.SUBSCRIPTION,
#         description=f"{item_type.replace('_',' ').title()} - {item_id}",
#         metadata={'checkout_session_id': session.id, 'payment_intent_id': payment_intent_id, 'subscription_id': subscription_id}
#     )
#     print(f"Payment record created (pending): {payment_record.id} for session {session.id}")
#
#     # If it's a subscription, the 'invoice.paid' event will typically confirm the recurring payment
#     # and update the user's subscription status.
#     # For one-off payments, 'payment_intent.succeeded' is more direct for success.
#
# def handle_payment_intent_succeeded(payment_intent):
#     """
#     Handles the 'payment_intent.succeeded' webhook event.
#     This confirms the payment was successful.
#     """
#     print(f"Payment intent succeeded: {payment_intent.id}")
#     checkout_session_id = payment_intent.get('metadata', {}).get('checkout_session_id') # If passed during PI creation
#     stripe_charge_id = payment_intent.charges.data[0].id if payment_intent.charges and payment_intent.charges.data else payment_intent.id
#
#     # Find the PaymentRecord. If checkout_session_id is in metadata, use it.
#     # Otherwise, try to find based on payment_intent_id stored in metadata if checkout session was first point of contact.
#     payment_record = None
#     if checkout_session_id: # This metadata needs to be set if PI is created outside checkout flow
#         payment_record = PaymentRecord.objects.filter(metadata__checkout_session_id=checkout_session_id).first()
#
#     if not payment_record: # Fallback: if checkout_session.completed created the record with session.id
#         payment_record = PaymentRecord.objects.filter(stripe_charge_id=payment_intent.invoice if payment_intent.invoice else payment_intent.latest_charge if payment_intent.latest_charge else payment_intent.id).first()
#         if not payment_record: # Try to find based on a PaymentRecord created by checkout.session.completed using the session.id
#              records_by_session = PaymentRecord.objects.filter(metadata__payment_intent_id=payment_intent.id)
#              if records_by_session.exists():
#                  payment_record = records_by_session.first() # Assuming one PI per session record
#              else: # Last resort: if the payment_intent itself was used as stripe_charge_id
#                  payment_record = PaymentRecord.objects.filter(stripe_charge_id=payment_intent.id).first()
#
#
#     if payment_record:
#         payment_record.status = PaymentRecord.PaymentStatus.SUCCESSFUL
#         payment_record.stripe_charge_id = stripe_charge_id # Update to actual charge ID
#         payment_record.metadata['payment_intent_id_confirmed'] = payment_intent.id
#         payment_record.save()
#         print(f"Payment record {payment_record.id} updated to SUCCESSFUL for PI {payment_intent.id}")
#
#         # Send audit signal and notification
#         payment_successful.send(sender=None, user=payment_record.user, payment_record=payment_record)
#         # TODO: Trigger email notification for successful payment
#         # from core.utils.email import send_payment_success_email
#         # send_payment_success_email(payment_record.user.email, payment_record)
#
#         # Update Provider's subscription tier if it's a subscription payment
#         if payment_record.payment_type == PaymentRecord.PaymentType.SUBSCRIPTION and payment_record.user.role == 'PROVIDER':
#             try:
#                 provider_profile = ProviderProfile.objects.get(user=payment_record.user)
#                 # Determine tier based on payment_record.description or metadata
#                 # This logic needs to be robust based on how you map price_ids to tiers
#                 if settings.STRIPE_PROVIDER_SUB_TIER1_PRICE_ID in payment_record.description: # Example
#                     provider_profile.subscription_tier = ProviderProfile.SubscriptionTier.PREMIUM # Or whatever tier it is
#                 # elif settings.STRIPE_PROVIDER_SUB_BASIC_PRICE_ID in payment_record.description:
#                 #     provider_profile.subscription_tier = ProviderProfile.SubscriptionTier.BASIC
#                 provider_profile.save()
#                 print(f"Provider {payment_record.user.email} subscription tier updated.")
#             except ProviderProfile.DoesNotExist:
#                 print(f"Error: ProviderProfile not found for user {payment_record.user.id} during subscription update.")
#     else:
#         print(f"Warning: No matching PaymentRecord found for payment_intent {payment_intent.id}. May need manual reconciliation.")
#
#
# def handle_invoice_paid(invoice):
#     """
#     Handles the 'invoice.paid' webhook event, typically for subscriptions.
#     """
#     print(f"Invoice paid: {invoice.id}")
#     customer_id = invoice.customer
#     subscription_id = invoice.subscription
#     charge_id = invoice.charge # The actual charge ID for this invoice payment
#
#     if not customer_id:
#         print(f"Error: Customer ID not found in invoice {invoice.id}")
#         return
#
#     # Find user by Stripe customer_id (you'd need to store this mapping, e.g., on User or Profile model)
#     # For now, we rely on user_id from checkout session metadata in PaymentRecord
#     # Or, if the payment_intent.succeeded already handled this payment, this might be redundant or just an update.
#
#     # Try to find existing payment record by subscription_id or create/update
#     # This logic can be complex depending on how you want to link recurring payments
#     payment_record = PaymentRecord.objects.filter(metadata__subscription_id=subscription_id, status=PaymentRecord.PaymentStatus.PENDING).order_by('-created_at').first()
#
#     if not payment_record: # If not found or already successful, create a new one for this recurring payment
#         # We need the user associated with this customer_id or subscription_id
#         # This requires storing stripe_customer_id on your User/Profile model,
#         # or getting user_id from the original checkout session metadata
#         # For MVP, we might rely on payment_intent.succeeded for the initial subscription.
#         # Subsequent invoice.paid events would update or create new records.
#         print(f"No pending PaymentRecord found for subscription {subscription_id} via invoice.paid. This might be a renewal.")
#         # If it's a renewal, we might need to create a new PaymentRecord.
#         # This requires robust mapping from customer_id/subscription_id back to your user.
#         # For simplicity, we focus on the initial setup via checkout.session.completed and payment_intent.succeeded.
#         # If payment_intent.succeeded for a subscription already created a PaymentRecord, this might be redundant.
#         # However, invoice.paid is crucial for ongoing subscription renewals.
#
#         # Let's assume that for the MVP, the initial subscription's payment_intent.succeeded is the primary trigger.
#         # If we are to handle renewals properly, we need to:
#         # 1. Store Stripe customer_id on User/Profile model during initial subscription.
#         # 2. When invoice.paid webhook comes, find User by customer_id.
#         # 3. Create a new PaymentRecord for this renewal.
#
#         # For now, check if a successful payment for this charge already exists
#         if charge_id and PaymentRecord.objects.filter(stripe_charge_id=charge_id, status=PaymentRecord.PaymentStatus.SUCCESSFUL).exists():
#             print(f"Payment for charge {charge_id} (invoice {invoice.id}) already recorded as successful.")
#             return
#         # If not, and we can identify the user, create a new record
#         # user = User.objects.get(stripe_customer_id=customer_id) # Hypothetical field
#         # if user:
#         #    PaymentRecord.objects.create(...)
#         return # Keep MVP simpler, focus on payment_intent.succeeded
#
#     if payment_record and payment_record.status == PaymentRecord.PaymentStatus.PENDING:
#         payment_record.status = PaymentRecord.PaymentStatus.SUCCESSFUL
#         payment_record.stripe_charge_id = charge_id or payment_record.stripe_charge_id # Update with actual charge ID if available
#         payment_record.metadata['invoice_id_confirmed'] = invoice.id
#         payment_record.save()
#         print(f"Payment record {payment_record.id} updated to SUCCESSFUL via invoice {invoice.id}")
#
#         # Send audit signal and notification
#         payment_successful.send(sender=None, user=payment_record.user, payment_record=payment_record)
#         # TODO: Trigger email notification for successful payment
#         # from core.utils.email import send_payment_success_email
#         # send_payment_success_email(payment_record.user.email, payment_record)
#
#         # Update Provider's subscription tier
#         if payment_record.user.role == 'PROVIDER':
#             try:
#                 provider_profile = ProviderProfile.objects.get(user=payment_record.user)
#                 # Determine tier (logic similar to handle_payment_intent_succeeded)
#                 if settings.STRIPE_PROVIDER_SUB_TIER1_PRICE_ID in payment_record.description: # Example
#                     provider_profile.subscription_tier = ProviderProfile.SubscriptionTier.PREMIUM
#                 provider_profile.save()
#                 print(f"Provider {payment_record.user.email} subscription tier updated via invoice.")
#             except ProviderProfile.DoesNotExist:
#                  print(f"Error: ProviderProfile not found for user {payment_record.user.id} during invoice-based subscription update.")
#     else:
#         print(f"Invoice {invoice.id} paid, but no matching PENDING PaymentRecord found or already processed.")
#
#
# def handle_payment_intent_payment_failed(payment_intent):
#     """
#     Handles the 'payment_intent.payment_failed' webhook event.
#     """
#     print(f"Payment intent failed: {payment_intent.id}")
#     # Find payment record (similar logic to succeeded)
#     # Update its status to FAILED
#     # payment_record.status = PaymentRecord.PaymentStatus.FAILED
#     # payment_record.save()
#     # TODO: Notify user of payment failure
#     # from core.utils.email import send_payment_failed_email
#     # send_payment_failed_email(user.email, payment_record)
#     pass # Implement full logic

# import stripe # No longer strictly needed for the simulated flow
from django.conf import settings
# from django.urls import reverse # Not needed for simulated success URL
from .models import PaymentRecord # Ensure this model exists
from users.models import User # Assuming your User model is in 'users.models'
import uuid # For generating dummy IDs

# stripe.api_key = settings.STRIPE_SECRET_KEY # This line is no longer essential for simulation

class PaymentService:
    def create_checkout_session(self, user, amount_in_cents, currency="usd", description="Service Payment", success_path="/payment/success", cancel_path="/payment/cancel"):
        """
        MODIFIED: Simulates a Stripe Checkout session creation and immediately fulfills the order.
        user: The Django user object.
        amount_in_cents: Amount in the smallest currency unit.
        currency: Currency code.
        description: Description of the payment.
        success_path: Frontend relative path for success (used for constructing a dummy redirect).
        cancel_path: Frontend relative path for cancellation (less relevant in always-success simulation).
        """
        print(f"SIMULATING payment for user: {user.username}, amount: {amount_in_cents} {currency}")

        try:
            # Directly "fulfill" the order as if payment was successful
            payment_record = self.fulfill_order_simulated(
                user=user,
                amount_in_cents=amount_in_cents,
                currency=currency,
                description=description
            )

            if payment_record:
                # Return a success-like response that the frontend can use to redirect
                # to its own success page. No actual Stripe session_id here.
                frontend_base_url = settings.NEXT_PUBLIC_APP_URL or "http://localhost:3000"
                simulated_success_url = f"{frontend_base_url}{success_path}?simulated_payment_id={payment_record.id}"

                return {
                    "status": "simulated_success",
                    "message": "Payment simulated successfully.",
                    "redirect_url": simulated_success_url, # Frontend can use this to navigate
                    "payment_record_id": payment_record.id
                }
            else:
                return {
                    "status": "simulation_error",
                    "message": "Failed to simulate payment and record order."
                }

        except Exception as e:
            print(f"Error during simulated payment processing: {e}")
            # Log the error e
            return {
                "status": "error",
                "message": f"An error occurred during payment simulation: {str(e)}"
            }

    def handle_webhook_event(self, payload, sig_header):
        """
        MODIFIED: This webhook will not be called in the simulated flow.
        If it were, it would do nothing or log that it's in simulation mode.
        """
        print("SIMULATION MODE: Stripe webhook endpoint hit, but no action taken as Stripe is not used.")
        # In a real scenario with Stripe disabled, this shouldn't be reached
        # unless something is misconfigured.
        # If you want to test the webhook endpoint structure, you could simulate an event here.
        return {"status": "simulated_webhook_received"}, 200

    def fulfill_order_simulated(self, user, amount_in_cents, currency, description):
        """
        MODIFIED: Called directly when a checkout session is "simulated" as completed.
        Creates a PaymentRecord with dummy data.
        """
        # Generate a dummy Stripe charge ID
        simulated_stripe_charge_id = f"sim_local_{uuid.uuid4()}"
        amount_decimal = amount_in_cents / 100.0 # Convert cents to dollars/euros

        print(f"SIMULATING FULFILLMENT: User ID: {user.id}, Amount: {amount_decimal} {currency.upper()}")

        try:
            payment_record = PaymentRecord.objects.create(
                user=user,
                stripe_charge_id=simulated_stripe_charge_id, # Use dummy ID
                amount=amount_decimal,
                currency=currency.upper(),
                status='succeeded', # Mark as succeeded
                description=description,
                # Add any other fields your PaymentRecord might have, e.g., payment_method
                payment_method='simulated_card'
            )
            print(f"Simulated PaymentRecord created: {payment_record.id}")

            # TODO: Add any other logic that should happen on successful payment
            # e.g., Granting user access to services, sending a confirmation email (simulated)
            # user.profile.is_premium = True
            # user.profile.save()

            return payment_record
        except User.DoesNotExist: # Should not happen if 'user' is passed correctly
            print(f"User with ID {user.id} not found for PaymentRecord (simulation).")
            return None
        except Exception as e:
            print(f"Error creating simulated PaymentRecord: {e}")
            # Log error `e`
            return None

    # The original fulfill_order (if it took a Stripe session object) would be
    # heavily modified or replaced by fulfill_order_simulated.
    # def fulfill_order(self, session):
    #   ... this logic is now mostly in fulfill_order_simulated ...