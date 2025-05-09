from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from .views import HealthCheckView # Ensure this view is created

urlpatterns = [
    path('admin/', admin.site.urls),
    path('healthz/', HealthCheckView.as_view(), name='health_check'),

    path('api/v1/auth/', include('users.urls')),
    path('api/v1/profiles/', include('profiles.urls')),
    path('api/v1/matching/', include('matching.urls')),
    path('api/v1/payments/', include('payments.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]