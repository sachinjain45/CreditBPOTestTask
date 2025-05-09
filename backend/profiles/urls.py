from django.urls import path
from .views import MyProfileView #, SeekerProfileDetailView, ProviderProfileDetailView

urlpatterns = [
    path('me/', MyProfileView.as_view(), name='my_profile'),
    # Add other profile-related URLs if needed for admin or specific access patterns
    # path('seekers/<int:pk>/', SeekerProfileDetailView.as_view(), name='seeker_profile_detail'),
    # path('providers/<int:pk>/', ProviderProfileDetailView.as_view(), name='provider_profile_detail'),
]