"""
Authentication serializers
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from apps.users.models import User


class LoginSerializer(serializers.Serializer):
    """
    Serializer pour le login avec téléphone et mot de passe
    """
    telephone = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        telephone = data.get('telephone')
        password = data.get('password')
        
        if not telephone or not password:
            raise serializers.ValidationError("Téléphone et mot de passe requis")
        
        # Authentifier l'utilisateur
        user = authenticate(username=telephone, password=password)
        
        if not user:
            raise serializers.ValidationError("Identifiants incorrects")
        
        if not user.is_active:
            raise serializers.ValidationError("Compte désactivé")
        
        data['user'] = user
        return data


class UserInfoSerializer(serializers.ModelSerializer):
    """
    Serializer pour les informations utilisateur
    """
    role_nom = serializers.CharField(source='role.get_nom_display', read_only=True)
    role_code = serializers.CharField(source='role.nom', read_only=True)
    nom_complet = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'telephone', 'nom', 'prenom', 'nom_complet',
            'role', 'role_nom', 'role_code',
            'is_staff', 'is_active', 'created_at'
        ]
        read_only_fields = fields
