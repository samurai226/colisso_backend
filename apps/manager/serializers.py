from rest_framework import serializers
from .models import DemandeFonds, MembreGare
from apps.users.serializers import UserSerializer
from apps.locations.models import Gare


class GareSimpleSerializer(serializers.ModelSerializer):
    """Serializer simple pour Gare (au cas où locations n'a pas de serializer)"""
    class Meta:
        model = Gare
        fields = ['id', 'nom', 'numero', 'contact']


class DemandeSerializer(serializers.ModelSerializer):
    responsable = UserSerializer(read_only=True)
    gare = GareSimpleSerializer(read_only=True)
    responsable_nom = serializers.CharField(source='responsable.nom_complet', read_only=True)
    gare_nom = serializers.CharField(source='gare.nom', read_only=True)
    
    class Meta:
        model = DemandeFonds
        fields = [
            'id', 'responsable', 'responsable_nom', 'gare', 'gare_nom',
            'montant', 'raison', 'statut', 'date_demande', 'date_traitement',
            'commentaire_admin'
        ]
        read_only_fields = ['id', 'date_demande', 'date_traitement']


class MembreGareSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    gare = GareSimpleSerializer(read_only=True)
    user_nom = serializers.CharField(source='user.nom_complet', read_only=True)
    gare_nom = serializers.CharField(source='gare.nom', read_only=True)
    ajout_par_nom = serializers.CharField(source='ajout_par.nom_complet', read_only=True)
    
    class Meta:
        model = MembreGare
        fields = [
            'id', 'user', 'user_nom', 'gare', 'gare_nom', 
            'date_ajout', 'ajout_par', 'ajout_par_nom', 'est_actif'
        ]
        read_only_fields = ['id', 'date_ajout']
