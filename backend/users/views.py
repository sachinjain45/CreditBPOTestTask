from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import UserRegistrationSerializer, UserDetailSerializer
from .models import User
from core.signals import user_registered # Import audit signal

# Custom permission classes (examples)
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff and request.user.role == 'ADMIN'

class IsSeekerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'SEEKER'

class IsProviderUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'PROVIDER'

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny] # Anyone can register

    def perform_create(self, serializer):
        user = serializer.save()
        # Send audit signal
        user_registered.send(sender=self.__class__, user=user, request=self.request)
        # TODO: Send welcome email via SendGrid (call utility function)
        # from core.utils.email import send_welcome_email
        # send_welcome_email(user.email, user.first_name or user.username)


class UserMeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    # If you want to allow updates to user details (e.g. first/last name)
    # def perform_update(self, serializer):
    #     serializer.save()


# You can customize TokenObtainPairView if needed, e.g., to add user role to token payload
# class MyTokenObtainPairView(TokenObtainPairView):
#     pass

# class MyTokenRefreshView(TokenRefreshView):
#     pass