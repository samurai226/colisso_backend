"""
URL Configuration for Colisso - Module 1
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API v1
    path('api/v1/', include('apps.core.urls')),
    path('api/v1/locations/', include('apps.locations.urls')),
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/parcels/', include('apps.parcels.urls')),
    path('api/v1/trips/', include('apps.trips.urls')),
    path('api/manager/', include('apps.manager.urls')),
    path('api/reservations/', include('apps.reservations.urls')),
]
