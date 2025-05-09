from rest_framework import generics, permissions
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page 
from django.conf import settings

from profiles.models import ProviderProfile
from .serializers import MatchResultSerializer
from users.models import Role
# Define a permission, e.g., only Seekers can search for matches
class IsSeekerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.role == Role.SEEKER or request.user.role == Role.ADMIN)


class MatchAPIView(generics.ListAPIView):
    serializer_class = MatchResultSerializer
    permission_classes = [permissions.IsAuthenticated, IsSeekerOrAdmin] # Or just IsAuthenticated

    def get_queryset(self):
        queryset = ProviderProfile.objects.filter(user__is_active=True) # Only active providers

        industry = self.request.query_params.get('industry')
        location = self.request.query_params.get('location')

        # Basic rule-based filtering
        # For JSONFields, you might need more complex queries or to denormalize
        if industry:
            # Assuming industry maps to one of the service_types
            # This is a simple contains check; might need better logic
            queryset = queryset.filter(service_types__icontains=industry)

        if location:
            # Assuming location can be part of geos_served or general location
            queryset = queryset.filter(
                Q(geos_served__icontains=location) | Q(location__icontains=location)
            )

        # Further filtering based on subscription_tier could be added
        # e.g., queryset = queryset.filter(subscription_tier__in=[ProviderProfile.SubscriptionTier.BASIC, ProviderProfile.SubscriptionTier.PREMIUM])

        return queryset.select_related('user').order_by('-subscription_tier', '-updated_at') # Premium first

    # Cache this view for 15 minutes (900 seconds)
    @method_decorator(cache_page(settings.CACHES['default']['TIMEOUT'] if 'TIMEOUT' in settings.CACHES['default'] else 60*15))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class MLMatchStubAPIView(MatchAPIView): # Inherits queryset logic and permissions
    """
    Stubbed ML hook that simply proxies to the rules-based endpoint logic.
    In a real scenario, this would call an ML service or model.
    """
    # No need to override anything if it just uses the same logic for now.
    # If caching is different or parameters, override get()
    pass