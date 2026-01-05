"""
Locations serializers
"""
from rest_framework import serializers
from .models import Pays, Ville, Quartier, Gare


class PaysSerializer(serializers.ModelSerializer):
    nombre_villes = serializers.SerializerMethodField()
    
    class Meta:
        model = Pays
        fields = ['id', 'nom', 'code', 'indicatif', 'nombre_villes', 'created_at', 'is_active']
        read_only_fields = ['id', 'created_at']
    
    def get_nombre_villes(self, obj):
        return obj.villes.filter(is_active=True).count()


class VilleSerializer(serializers.ModelSerializer):
    pays_nom = serializers.CharField(source='pays.nom', read_only=True)
    nombre_quartiers = serializers.SerializerMethodField()
    
    class Meta:
        model = Ville
        fields = ['id', 'nom', 'pays', 'pays_nom', 'population', 'nombre_quartiers', 'created_at', 'is_active']
        read_only_fields = ['id', 'created_at']
    
    def get_nombre_quartiers(self, obj):
        return obj.quartiers.filter(is_active=True).count()


class QuartierSerializer(serializers.ModelSerializer):
    ville_nom = serializers.CharField(source='ville.nom', read_only=True)
    nombre_gares = serializers.SerializerMethodField()
    
    class Meta:
        model = Quartier
        fields = ['id', 'nom', 'ville', 'ville_nom', 'nombre_gares', 'created_at', 'is_active']
        read_only_fields = ['id', 'created_at']
    
    def get_nombre_gares(self, obj):
        return obj.gares.filter(is_active=True).count()


class GareSerializer(serializers.ModelSerializer):
    quartier_nom = serializers.CharField(source='quartier.nom', read_only=True)
    ville_nom = serializers.CharField(source='quartier.ville.nom', read_only=True)
    pays_nom = serializers.CharField(source='quartier.ville.pays.nom', read_only=True)
    
    class Meta:
        model = Gare
        fields = [
            'id', 'nom', 'quartier', 'quartier_nom', 'ville_nom', 'pays_nom',
            'adresse', 'telephone', 'latitude', 'longitude',
            'created_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at']


class GareDetailSerializer(GareSerializer):
    """Serializer détaillé pour une gare avec infos complètes"""
    quartier_detail = QuartierSerializer(source='quartier', read_only=True)
    
    class Meta(GareSerializer.Meta):
        fields = GareSerializer.Meta.fields + ['quartier_detail']
