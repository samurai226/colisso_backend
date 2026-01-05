"""
Users viewsets
"""
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Role, User, AffectationGare
from .serializers import (
    RoleSerializer, UserSerializer, UserDetailSerializer,
    AffectationGareSerializer
)


class RoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les Rôles
    """
    queryset = Role.objects.filter(is_active=True)
    serializer_class = RoleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom', 'description']
    ordering_fields = ['nom', 'created_at']
    ordering = ['nom']


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les Utilisateurs
    """
    queryset = User.objects.filter(is_active=True).select_related('role')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_staff']
    search_fields = ['nom', 'prenom', 'telephone']
    ordering_fields = ['nom', 'prenom', 'created_at']
    ordering = ['nom']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer


class AffectationGareViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les Affectations Gare
    """
    queryset = AffectationGare.objects.filter(is_active=True).select_related(
        'user', 'gare', 'gare__quartier', 'gare__quartier__ville'
    )
    serializer_class = AffectationGareSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'gare', 'est_principale']
    search_fields = ['user__nom', 'user__prenom', 'gare__nom']
    ordering_fields = ['date_debut', 'created_at']
    ordering = ['-date_debut']
