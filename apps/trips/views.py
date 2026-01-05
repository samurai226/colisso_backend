from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from django.utils import timezone
from django.db.models import Q, F

from .models import Trajet, Reservation
from .serializers import (
    TrajetSerializer, 
    TrajetListSerializer,
    ReservationSerializer, 
    ReservationListSerializer,
    ValidationReservationSerializer
)


class TrajetViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les trajets
    
    Liste tous les trajets disponibles avec filtres
    Lecture publique autorisée, modification nécessite authentification
    """
    queryset = Trajet.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]  # Lecture publique, écriture authentifiée
    
    def get_serializer_class(self):
        """Utilise un serializer simplifié pour la liste"""
        if self.action == 'list':
            return TrajetListSerializer
        return TrajetSerializer
    
    def get_queryset(self):
        """
        Filtre les trajets selon les paramètres de requête
        """
        queryset = Trajet.objects.all()
        
        # Filtre par statut (par défaut: seulement les planifiés)
        statut = self.request.query_params.get('statut', 'planifie')
        if statut:
            queryset = queryset.filter(statut=statut)
        
        # Filtre par date
        date_depart = self.request.query_params.get('date_depart')
        if date_depart:
            queryset = queryset.filter(date_depart=date_depart)
        
        # Filtre par ville de départ
        ville_depart = self.request.query_params.get('ville_depart')
        if ville_depart:
            queryset = queryset.filter(ville_depart__icontains=ville_depart)
        
        # Filtre par ville d'arrivée
        ville_arrivee = self.request.query_params.get('ville_arrivee')
        if ville_arrivee:
            queryset = queryset.filter(ville_arrivee__icontains=ville_arrivee)
        
        # Filtre par type (VIP ou non)
        is_vip = self.request.query_params.get('is_vip')
        if is_vip is not None:
            queryset = queryset.filter(is_vip=is_vip.lower() == 'true')
        
        # Seulement les trajets avec places disponibles
        disponible_uniquement = self.request.query_params.get('disponible')
        if disponible_uniquement and disponible_uniquement.lower() == 'true':
            queryset = queryset.filter(places_reservees__lt=F('capacite_max'))
        
        return queryset.order_by('-date_depart', '-heure_depart')
    
    @action(detail=True, methods=['get'])
    def reservations(self, request, pk=None):
        """
        Récupère toutes les réservations pour un trajet donné
        """
        trajet = self.get_object()
        reservations = Reservation.objects.filter(trajet_id=trajet.id)
        serializer = ReservationListSerializer(reservations, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def statistiques(self, request, pk=None):
        """
        Récupère les statistiques d'un trajet
        """
        trajet = self.get_object()
        reservations = Reservation.objects.filter(trajet_id=trajet.id)
        
        stats = {
            'capacite_max': trajet.capacite_max,
            'places_reservees': trajet.places_reservees,
            'places_disponibles': trajet.places_disponibles,
            'taux_occupation': trajet.taux_occupation,
            'nombre_reservations': reservations.count(),
            'reservations_payees': reservations.filter(statut__in=['payee', 'validee']).count(),
            'reservations_validees': reservations.filter(statut='validee').count(),
        }
        
        return Response(stats)


class ReservationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les réservations
    """
    queryset = Reservation.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Utilise un serializer simplifié pour la liste"""
        if self.action == 'list':
            return ReservationListSerializer
        elif self.action == 'valider':
            return ValidationReservationSerializer
        return ReservationSerializer
    
    def get_queryset(self):
        """
        Filtre les réservations selon les paramètres de requête
        """
        queryset = Reservation.objects.all()
        
        # Filtre par trajet
        trajet_id = self.request.query_params.get('trajet_id')
        if trajet_id:
            queryset = queryset.filter(trajet_id=trajet_id)
        
        # Filtre par statut
        statut = self.request.query_params.get('statut')
        if statut:
            queryset = queryset.filter(statut=statut)
        
        # Filtre par téléphone du client
        telephone = self.request.query_params.get('telephone')
        if telephone:
            queryset = queryset.filter(client_telephone=telephone)
        
        # Filtre par numéro de ticket
        numero_ticket = self.request.query_params.get('numero_ticket')
        if numero_ticket:
            queryset = queryset.filter(numero_ticket=numero_ticket)
        
        return queryset.order_by('-date_reservation')
    
    def perform_create(self, serializer):
        """
        Crée une nouvelle réservation et met à jour le trajet
        """
        reservation = serializer.save()
        
        # Mettre à jour le nombre de places réservées du trajet
        try:
            trajet = Trajet.objects.get(id=reservation.trajet_id)
            trajet.places_reservees += 1
            trajet.save()
        except Trajet.DoesNotExist:
            pass
    
    @action(detail=True, methods=['post'])
    def valider(self, request, pk=None):
        """
        Valide une réservation (pour les guichetiers)
        """
        reservation = self.get_object()
        
        if reservation.is_validee:
            return Response(
                {'error': 'Cette réservation a déjà été validée.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if reservation.statut == 'annulee':
            return Response(
                {'error': 'Cette réservation a été annulée.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Valider la réservation
        reservation.valider()
        
        serializer = self.get_serializer(reservation)
        return Response({
            'message': 'Réservation validée avec succès.',
            'reservation': serializer.data
        })
    
    @action(detail=False, methods=['post'])
    def valider_par_ticket(self, request):
        """
        Valide une réservation par son numéro de ticket
        """
        serializer = ValidationReservationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        numero_ticket = serializer.validated_data['numero_ticket']
        
        try:
            reservation = Reservation.objects.get(numero_ticket=numero_ticket)
            reservation.valider()
            
            return Response({
                'message': 'Ticket validé avec succès.',
                'reservation': ReservationSerializer(reservation).data
            })
        except Reservation.DoesNotExist:
            return Response(
                {'error': 'Ticket non trouvé.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def annuler(self, request, pk=None):
        """
        Annule une réservation
        """
        reservation = self.get_object()
        
        if reservation.is_validee:
            return Response(
                {'error': 'Impossible d\'annuler une réservation déjà validée.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Annuler la réservation
        reservation.statut = 'annulee'
        reservation.save()
        
        # Mettre à jour le nombre de places réservées du trajet
        try:
            trajet = Trajet.objects.get(id=reservation.trajet_id)
            trajet.places_reservees = max(0, trajet.places_reservees - 1)
            trajet.save()
        except Trajet.DoesNotExist:
            pass
        
        serializer = self.get_serializer(reservation)
        return Response({
            'message': 'Réservation annulée avec succès.',
            'reservation': serializer.data
        })
