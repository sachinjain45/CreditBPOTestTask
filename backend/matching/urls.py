from django.urls import path
from .views import MatchAPIView, MLMatchStubAPIView

urlpatterns = [
    path('', MatchAPIView.as_view(), name='get_matches'),
    path('ml/', MLMatchStubAPIView.as_view(), name='ml_get_matches_stub'),
]