from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DemandeViewSet, MembreGareViewSet

router = DefaultRouter()
router.register(r'demandes', DemandeViewSet, basename='demande')
router.register(r'membres', MembreGareViewSet, basename='membre')

urlpatterns = [
    path('', include(router.urls)),
]
