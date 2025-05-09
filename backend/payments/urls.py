# from django.urls import path
# from .views import CreateCheckoutSessionView, stripe_webhook_view, MyPaymentHistoryView #, ManageSubscriptionView
#
# urlpatterns = [
#     path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
#     path('webhook/', stripe_webhook_view, name='stripe_webhook'), # This is not an APIView
#     path('history/', MyPaymentHistoryView.as_view(), name='payment_history'),
#     # path('manage-subscription/', ManageSubscriptionView.as_view(), name='manage_subscription'),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'subscription', views.SubscriptionViewSet, basename='subscription')
router.register(r'payments', views.PaymentViewSet, basename='payment')
router.register(r'payment-methods', views.PaymentMethodViewSet, basename='payment-method')

urlpatterns = [
    path('', include(router.urls)),
]