from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import DemandeFonds, MembreGare
from .serializers import DemandeSerializer, MembreGareSerializer
from apps.users.models import User
from apps.locations.models import Gare


class DemandeViewSet(viewsets.ModelViewSet):
    """ViewSet pour les demandes de fonds"""
    serializer_class = DemandeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # Si responsable, voir seulement ses demandes
        if user.role and user.role.nom.lower() == 'responsable':
            return DemandeFonds.objects.filter(responsable=user)
        # Si admin, voir toutes les demandes
        return DemandeFonds.objects.all()
    
    def perform_create(self, serializer):
        # Le responsable crée la demande pour sa gare
        serializer.save(
            responsable=self.request.user,
            gare=self.request.user.gare
        )
    
    @action(detail=True, methods=['post'])
    def approuver(self, request, pk=None):
        """Approuver une demande (admin seulement)"""
        demande = self.get_object()
        demande.statut = 'approuvee'
        demande.date_traitement = timezone.now()
        demande.commentaire_admin = request.data.get('commentaire', '')
        demande.save()
        return Response({'message': 'Demande approuvée'})
    
    @action(detail=True, methods=['post'])
    def rejeter(self, request, pk=None):
        """Rejeter une demande (admin seulement)"""
        demande = self.get_object()
        demande.statut = 'rejetee'
        demande.date_traitement = timezone.now()
        demande.commentaire_admin = request.data.get('commentaire', '')
        demande.save()
        return Response({'message': 'Demande rejetée'})


class MembreGareViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des membres de gare"""
    serializer_class = MembreGareSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # Si responsable, voir seulement les membres de sa gare
        if user.role and user.role.nom.lower() == 'responsable' and user.gare:
            return MembreGare.objects.filter(gare=user.gare)
        # Si admin, voir tous les membres
        return MembreGare.objects.all()
    
    def create(self, request, *args, **kwargs):
        """Ajouter un membre à la gare"""
        user_id = request.data.get('user_id')
        gare_id = request.data.get('gare_id')
        
        try:
            user = User.objects.get(id=user_id)
            gare = Gare.objects.get(id=gare_id)
            
            # Vérifier si le membre existe déjà
            if MembreGare.objects.filter(user=user, gare=gare).exists():
                return Response(
                    {'error': 'Ce membre est déjà associé à cette gare'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Créer l'association
            membre = MembreGare.objects.create(
                user=user,
                gare=gare,
                ajout_par=request.user
            )
            
            serializer = self.get_serializer(membre)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except User.DoesNotExist:
            return Response(
                {'error': 'Utilisateur introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Gare.DoesNotExist:
            return Response(
                {'error': 'Gare introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def desactiver(self, request, pk=None):
        """Désactiver un membre"""
        membre = self.get_object()
        membre.est_actif = False
        membre.save()
        return Response({'message': 'Membre désactivé'})
    
    @action(detail=True, methods=['post'])
    def activer(self, request, pk=None):
        """Activer un membre"""
        membre = self.get_object()
        membre.est_actif = True
        membre.save()
        return Response({'message': 'Membre activé'})
