from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegistrationView, UserMeView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Default JWT login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Default JWT refresh
    path('me/', UserMeView.as_view(), name='user_me'),
]