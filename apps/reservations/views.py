from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from .models import Reservation
from .serializers import ReservationSerializer, ReservationCreateSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    """ViewSet pour les réservations/tickets"""
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ReservationCreateSerializer
        return ReservationSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        # Client : voir seulement ses réservations
        if user.role and user.role.nom.lower() == 'client':
            return Reservation.objects.filter(client=user)
        
        # Responsable/Guichetier : voir les réservations de leur gare
        if user.role and user.role.nom.lower() in ['responsable', 'guichetier']:
            if user.gare:
                return Reservation.objects.filter(
                    trajet__gare_depart=user.gare
                ) | Reservation.objects.filter(
                    trajet__gare_arrivee=user.gare
                )
        
        # Admin : voir toutes les réservations
        return Reservation.objects.all()
    
    def get_permissions(self):
        # Liste publique pour voir les réservations disponibles
        if self.action == 'list':
            return [AllowAny()]
        return super().get_permissions()
    
    @action(detail=True, methods=['post'])
    def valider(self, request, pk=None):
        """Valider un ticket (guichetier/responsable)"""
        reservation = self.get_object()
        reservation.statut = 'valide'
        reservation.date_validation = timezone.now()
        reservation.valide_par = request.user
        reservation.save()
        serializer = self.get_serializer(reservation)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def confirmer(self, request, pk=None):
        """Confirmer un ticket (après paiement)"""
        reservation = self.get_object()
        reservation.statut = 'confirme'
        reservation.save()
        serializer = self.get_serializer(reservation)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def annuler(self, request, pk=None):
        """Annuler un ticket"""
        reservation = self.get_object()
        reservation.statut = 'annule'
        reservation.save()
        serializer = self.get_serializer(reservation)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def par_trajet(self, request):
        """Obtenir les réservations pour un trajet spécifique"""
        trajet_id = request.query_params.get('trajet_id')
        if not trajet_id:
            return Response(
                {'error': 'trajet_id requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reservations = self.get_queryset().filter(trajet_id=trajet_id)
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)
