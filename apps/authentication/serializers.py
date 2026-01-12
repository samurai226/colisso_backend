"""
Authentication serializers
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from apps.users.models import User, Role


class RegisterSerializer(serializers.Serializer):
    """
    Serializer pour l'inscription - Le rôle CLIENT est automatique
    """
    telephone = serializers.CharField(required=True, max_length=20)
    nom = serializers.CharField(required=True, max_length=100)
    prenom = serializers.CharField(required=True, max_length=100)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=6
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    def validate_telephone(self, value):
        """Valider que le téléphone n'existe pas déjà"""
        if User.objects.filter(telephone=value).exists():
            raise serializers.ValidationError(
                "Ce numéro de téléphone est déjà utilisé."
            )
        return value
    
    def validate_email(self, value):
        """Valider que l'email n'existe pas déjà (si fourni)"""
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Cette adresse email est déjà utilisée."
            )
        return value
    
    def validate_password(self, value):
        """Valider le mot de passe avec les règles Django"""
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value
    
    def validate(self, attrs):
        """Valider que les mots de passe correspondent"""
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({
                "password_confirm": "Les mots de passe ne correspondent pas."
            })
        return attrs
    
    def create(self, validated_data):
        """Créer un utilisateur avec rôle CLIENT automatique"""
        # Retirer password_confirm (pas dans le modèle)
        validated_data.pop('password_confirm')
        
        # Récupérer ou créer le rôle CLIENT
        role_client, _ = Role.objects.get_or_create(
            nom=Role.CLIENT,
            defaults={'description': 'Client standard', 'is_active': True}
        )
        
        # Créer l'utilisateur
        user = User.objects.create_user(
            telephone=validated_data['telephone'],
            password=validated_data['password'],
            nom=validated_data['nom'],
            prenom=validated_data['prenom'],
            email=validated_data.get('email', ''),
            role=role_client,
            is_active=True
        )
        
        return user


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
            'id', 
            'telephone', 
            'nom', 
            'prenom', 
            'nom_complet',
            'email',
            'role', 
            'role_nom', 
            'role_code',
            'is_staff', 
            'is_active', 
            'created_at'
        ]
        read_only_fields = fields