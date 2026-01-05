"""
Parcels viewsets
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Colis, Livraison, HistoriqueEtat
from .serializers import (
    ColisSerializer, ColisDetailSerializer, ColisTrackingSerializer,
    LivraisonSerializer, HistoriqueEtatSerializer
)


class ColisViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les Colis
    """
    queryset = Colis.objects.filter(is_active=True).select_related(
        'expediteur', 'gare_depart', 'gare_arrivee'
    )
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['statut', 'expediteur', 'gare_depart', 'gare_arrivee']
    search_fields = ['code_suivi', 'destinataire_nom', 'destinataire_telephone']
    ordering_fields = ['date_expedition', 'date_arrivee_prevue', 'prix']
    ordering = ['-date_expedition']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ColisDetailSerializer
        elif self.action == 'tracking':
            return ColisTrackingSerializer
        return ColisSerializer
    
    def perform_create(self, serializer):
        # Générer un code de suivi unique
        import uuid
        code_suivi = f"COL-{uuid.uuid4().hex[:8].upper()}"
        
        colis = serializer.save(code_suivi=code_suivi)
        
        # Créer l'historique initial
        HistoriqueEtat.objects.create(
            colis=colis,
            ancien_statut=None,
            nouveau_statut=colis.statut,
            utilisateur=self.request.user if self.request.user.is_authenticated else None,
            commentaire="Colis créé",
            localisation=colis.gare_depart
        )
    
    @action(detail=True, methods=['post'])
    def changer_statut(self, request, pk=None):
        """Changer le statut d'un colis"""
        colis = self.get_object()
        nouveau_statut = request.data.get('statut')
        commentaire = request.data.get('commentaire', '')
        
        if nouveau_statut not in dict(Colis.STATUT_CHOICES):
            return Response(
                {'error': 'Statut invalide'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ancien_statut = colis.statut
        colis.statut = nouveau_statut
        
        # Mettre à jour les dates selon le statut
        if nouveau_statut == Colis.ARRIVE:
            colis.date_arrivee_reelle = timezone.now()
        elif nouveau_statut == Colis.LIVRE:
            colis.date_livraison = timezone.now()
        
        colis.save()
        
        # Créer l'historique
        HistoriqueEtat.objects.create(
            colis=colis,
            ancien_statut=ancien_statut,
            nouveau_statut=nouveau_statut,
            utilisateur=request.user,
            commentaire=commentaire,
            localisation=colis.gare_arrivee
        )
        
        return Response({'message': 'Statut changé avec succès'})
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def tracking(self, request):
        """Tracking public par code de suivi"""
        code_suivi = request.query_params.get('code')
        
        if not code_suivi:
            return Response(
                {'error': 'Code de suivi requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            colis = Colis.objects.prefetch_related('historique').get(
                code_suivi=code_suivi
            )
            serializer = ColisTrackingSerializer(colis)
            return Response(serializer.data)
        except Colis.DoesNotExist:
            return Response(
                {'error': 'Colis non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        """Statistiques des colis"""
        total = self.queryset.count()
        par_statut = {}
        
        for statut, _ in Colis.STATUT_CHOICES:
            par_statut[statut] = self.queryset.filter(statut=statut).count()
        
        return Response({
            'total': total,
            'par_statut': par_statut
        })


class LivraisonViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les Livraisons
    """
    queryset = Livraison.objects.filter(is_active=True).select_related(
        'colis', 'livreur'
    )
    serializer_class = LivraisonSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['statut', 'livreur', 'colis']
    search_fields = ['colis__code_suivi', 'livreur__nom', 'livreur__prenom']
    ordering_fields = ['date_assignation', 'date_fin']
    ordering = ['-date_assignation']
    
    @action(detail=True, methods=['post'])
    def assigner(self, request, pk=None):
        """Assigner un livreur"""
        livraison = self.get_object()
        livreur_id = request.data.get('livreur')
        
        if not livreur_id:
            return Response(
                {'error': 'Livreur requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from apps.users.models import User
        try:
            livreur = User.objects.get(id=livreur_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'Livreur non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        livraison.livreur = livreur
        livraison.statut = Livraison.ASSIGNEE
        livraison.date_assignation = timezone.now()
        livraison.save()
        
        return Response({'message': 'Livreur assigné avec succès'})
    
    @action(detail=True, methods=['post'])
    def demarrer(self, request, pk=None):
        """Démarrer la livraison"""
        livraison = self.get_object()
        livraison.statut = Livraison.EN_COURS
        livraison.date_debut = timezone.now()
        livraison.save()
        
        # Mettre à jour le colis
        livraison.colis.statut = Colis.EN_LIVRAISON
        livraison.colis.save()
        
        return Response({'message': 'Livraison démarrée'})
    
    @action(detail=True, methods=['post'])
    def terminer(self, request, pk=None):
        """Terminer la livraison (succès ou échec)"""
        livraison = self.get_object()
        succes = request.data.get('succes', True)
        
        livraison.date_fin = timezone.now()
        
        if succes:
            livraison.statut = Livraison.LIVREE
            livraison.signature_destinataire = request.data.get('signature', '')
            livraison.photo_livraison = request.data.get('photo', '')
            livraison.commentaire_livreur = request.data.get('commentaire', '')
            
            # Mettre à jour le colis
            livraison.colis.statut = Colis.LIVRE
            livraison.colis.date_livraison = timezone.now()
            livraison.colis.save()
        else:
            livraison.statut = Livraison.ECHEC
            livraison.raison_echec = request.data.get('raison', '')
            
            # Mettre à jour le colis
            livraison.colis.statut = Colis.PROBLEME
            livraison.colis.save()
        
        livraison.save()
        
        return Response({'message': 'Livraison terminée'})
    
    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        """Livraisons disponibles (en attente)"""
        livraisons = self.queryset.filter(statut=Livraison.EN_ATTENTE)
        serializer = self.get_serializer(livraisons, many=True)
        return Response(serializer.data)


class HistoriqueEtatViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour l'Historique (lecture seule)
    """
    queryset = HistoriqueEtat.objects.filter(is_active=True).select_related(
        'colis', 'utilisateur', 'localisation'
    )
    serializer_class = HistoriqueEtatSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['colis', 'nouveau_statut']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
