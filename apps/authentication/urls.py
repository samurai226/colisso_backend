"""
Authentication URLs
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, MeView

urlpatterns = [
    # Inscription
    path('register/', RegisterView.as_view(), name='register'),
    
    # Connexion
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User info
    path('me/', MeView.as_view(), name='me'),
]