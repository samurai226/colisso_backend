"""
URL Configuration for Colisso - Module 1
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def api_root(request):
    """API root endpoint"""
    return JsonResponse({
        'message': 'Colisso API v1',
        'version': '1.0.0',
        'documentation': {
            'swagger': request.build_absolute_uri('/api/schema/swagger-ui/'),
            'redoc': request.build_absolute_uri('/api/schema/redoc/'),
        },
        'endpoints': {
            'auth': '/api/v1/auth/',
            'users': '/api/v1/users/',
            'locations': '/api/v1/locations/',
            'parcels': '/api/v1/parcels/',
            'trips': '/api/v1/trips/',
            'reservations': '/api/v1/reservations/',
            'manager': '/api/v1/manager/',
        }
    })

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Root
    path('api/', api_root, name='api-root'),
    
    # API Schema & Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API v1 - Tous avec v1 pour cohérence
    path('api/v1/', include('apps.core.urls')),
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/locations/', include('apps.locations.urls')),
    path('api/v1/parcels/', include('apps.parcels.urls')),
    path('api/v1/trips/', include('apps.trips.urls')),
    path('api/v1/reservations/', include('apps.reservations.urls')),
    path('api/v1/manager/', include('apps.manager.urls')),
]