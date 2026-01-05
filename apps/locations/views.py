"""
Locations viewsets
"""
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Pays, Ville, Quartier, Gare
from .serializers import (
    PaysSerializer, VilleSerializer, QuartierSerializer,
    GareSerializer, GareDetailSerializer
)


class PaysViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les Pays
    """
    queryset = Pays.objects.filter(is_active=True)
    serializer_class = PaysSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['code']
    search_fields = ['nom', 'code']
    ordering_fields = ['nom', 'created_at']
    ordering = ['nom']


class VilleViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les Villes
    """
    queryset = Ville.objects.filter(is_active=True).select_related('pays')
    serializer_class = VilleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['pays']
    search_fields = ['nom']
    ordering_fields = ['nom', 'population', 'created_at']
    ordering = ['nom']


class QuartierViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les Quartiers
    """
    queryset = Quartier.objects.filter(is_active=True).select_related('ville', 'ville__pays')
    serializer_class = QuartierSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ville']
    search_fields = ['nom']
    ordering_fields = ['nom', 'created_at']
    ordering = ['nom']


class GareViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les Gares
    """
    queryset = Gare.objects.filter(is_active=True).select_related(
        'quartier', 'quartier__ville', 'quartier__ville__pays'
    )
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['quartier', 'quartier__ville']
    search_fields = ['nom', 'adresse']
    ordering_fields = ['nom', 'created_at']
    ordering = ['nom']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GareDetailSerializer
        return GareSerializer
