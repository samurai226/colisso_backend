from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrajetViewSet, ReservationViewSet

# Créer un router et enregistrer les ViewSets
router = DefaultRouter()
router.register(r'trajets', TrajetViewSet, basename='trajet')
router.register(r'reservations', ReservationViewSet, basename='reservation')

app_name = 'trips'

urlpatterns = [
    path('', include(router.urls)),
]
