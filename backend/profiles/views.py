from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import SeekerProfile, ProviderProfile
from .serializers import SeekerProfileSerializer, ProviderProfileSerializer
from users.models import Role
from core.signals import profile_updated # For audit log

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    Assumes the model has a 'user' foreign key.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the profile or an admin.
        return obj.user == request.user or request.user.role == Role.ADMIN


class MyProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_serializer_class(self):
        if self.request.user.role == Role.SEEKER:
            return SeekerProfileSerializer
        elif self.request.user.role == Role.PROVIDER:
            return ProviderProfileSerializer
        return None # Should not happen if user has a role

    def get_object(self):
        user = self.request.user
        try:
            if user.role == Role.SEEKER:
                return SeekerProfile.objects.get(user=user)
            elif user.role == Role.PROVIDER:
                return ProviderProfile.objects.get(user=user)
        except (SeekerProfile.DoesNotExist, ProviderProfile.DoesNotExist):
            # This can happen if the signal to create profile failed or user role changed
            # For robustness, you might want to create it here if it doesn't exist
            # Or ensure the signal handler in apps.py always creates it.
            return None
        return None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({"detail": "Profile not found for this user."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if not instance:
            return Response({"detail": "Profile not found for this user."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Send audit signal
        profile_updated.send(sender=self.__class__, user=request.user, profile=instance, request=request)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been used, then clear the cache.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

# Generic views for Admin CRUD if needed, but MyProfileView is primary for users
# class SeekerProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = SeekerProfile.objects.all()
#     serializer_class = SeekerProfileSerializer
#     permission_classes = [permissions.IsAdminUser] # Example: Only Admins

# class ProviderProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = ProviderProfile.objects.all()
#     serializer_class = ProviderProfileSerializer
#     permission_classes = [permissions.IsAdminUser] # Example