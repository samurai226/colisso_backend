"""
Parcels URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ColisViewSet, LivraisonViewSet, HistoriqueEtatViewSet

router = DefaultRouter()
router.register(r'colis', ColisViewSet, basename='colis')
router.register(r'livraisons', LivraisonViewSet, basename='livraison')
router.register(r'historique', HistoriqueEtatViewSet, basename='historique')

urlpatterns = [
    path('', include(router.urls)),
]
