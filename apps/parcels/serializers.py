"""
Parcels serializers
"""
from rest_framework import serializers
from .models import Colis, Livraison, HistoriqueEtat


class HistoriqueEtatSerializer(serializers.ModelSerializer):
    ancien_statut_display = serializers.CharField(
        source='get_ancien_statut_display',
        read_only=True
    )
    nouveau_statut_display = serializers.CharField(
        source='get_nouveau_statut_display',
        read_only=True
    )
    utilisateur_nom = serializers.CharField(
        source='utilisateur.nom_complet',
        read_only=True
    )
    localisation_nom = serializers.CharField(
        source='localisation.nom',
        read_only=True
    )
    
    class Meta:
        model = HistoriqueEtat
        fields = [
            'id', 'colis', 'ancien_statut', 'ancien_statut_display',
            'nouveau_statut', 'nouveau_statut_display',
            'utilisateur', 'utilisateur_nom',
            'commentaire', 'localisation', 'localisation_nom',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class LivraisonSerializer(serializers.ModelSerializer):
    statut_display = serializers.CharField(
        source='get_statut_display',
        read_only=True
    )
    livreur_nom = serializers.CharField(
        source='livreur.nom_complet',
        read_only=True
    )
    colis_code = serializers.CharField(
        source='colis.code_suivi',
        read_only=True
    )
    
    class Meta:
        model = Livraison
        fields = [
            'id', 'colis', 'colis_code', 'livreur', 'livreur_nom',
            'statut', 'statut_display',
            'date_assignation', 'date_debut', 'date_fin',
            'signature_destinataire', 'photo_livraison',
            'commentaire_livreur', 'raison_echec',
            'created_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at']


class ColisSerializer(serializers.ModelSerializer):
    statut_display = serializers.CharField(
        source='get_statut_display',
        read_only=True
    )
    expediteur_nom = serializers.CharField(
        source='expediteur.nom_complet',
        read_only=True
    )
    gare_depart_nom = serializers.CharField(
        source='gare_depart.nom',
        read_only=True
    )
    gare_arrivee_nom = serializers.CharField(
        source='gare_arrivee.nom',
        read_only=True
    )
    est_paye = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Colis
        fields = [
            'id', 'code_suivi', 'description', 'poids', 'valeur_declaree',
            'expediteur', 'expediteur_nom',
            'destinataire_nom', 'destinataire_telephone', 'destinataire_adresse',
            'gare_depart', 'gare_depart_nom',
            'gare_arrivee', 'gare_arrivee_nom',
            'statut', 'statut_display',
            'prix', 'montant_paye', 'est_paye',
            'date_expedition', 'date_arrivee_prevue',
            'date_arrivee_reelle', 'date_livraison',
            'notes', 'created_at', 'is_active'
        ]
        read_only_fields = ['id', 'code_suivi', 'date_expedition', 'created_at']


class ColisDetailSerializer(ColisSerializer):
    """Serializer détaillé avec historique et livraisons"""
    historique = HistoriqueEtatSerializer(many=True, read_only=True)
    livraisons = LivraisonSerializer(many=True, read_only=True)
    
    class Meta(ColisSerializer.Meta):
        fields = ColisSerializer.Meta.fields + ['historique', 'livraisons']


class ColisTrackingSerializer(serializers.ModelSerializer):
    """Serializer pour le tracking public (sans infos sensibles)"""
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    gare_depart_nom = serializers.CharField(source='gare_depart.nom', read_only=True)
    gare_arrivee_nom = serializers.CharField(source='gare_arrivee.nom', read_only=True)
    historique = HistoriqueEtatSerializer(many=True, read_only=True)
    
    class Meta:
        model = Colis
        fields = [
            'code_suivi', 'statut', 'statut_display',
            'gare_depart_nom', 'gare_arrivee_nom',
            'date_expedition', 'date_arrivee_prevue',
            'date_arrivee_reelle', 'date_livraison',
            'historique'
        ]
