"""
Users serializers
"""
from rest_framework import serializers
from .models import Role, User, AffectationGare


class RoleSerializer(serializers.ModelSerializer):
    nombre_users = serializers.SerializerMethodField()
    
    class Meta:
        model = Role
        fields = ['id', 'nom', 'description', 'nombre_users', 'created_at', 'is_active']
        read_only_fields = ['id', 'created_at']
    
    def get_nombre_users(self, obj):
        return obj.users.filter(is_active=True).count()


class UserSerializer(serializers.ModelSerializer):
    role_nom = serializers.CharField(source='role.get_nom_display', read_only=True)
    nom_complet = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = [
            'id', 'telephone', 'nom', 'prenom', 'nom_complet',
            'role', 'role_nom', 'password',
            'is_staff', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class AffectationGareSerializer(serializers.ModelSerializer):
    user_nom = serializers.CharField(source='user.nom_complet', read_only=True)
    gare_nom = serializers.CharField(source='gare.nom', read_only=True)
    ville_nom = serializers.CharField(source='gare.quartier.ville.nom', read_only=True)
    
    class Meta:
        model = AffectationGare
        fields = [
            'id', 'user', 'user_nom', 'gare', 'gare_nom', 'ville_nom',
            'date_debut', 'date_fin', 'est_principale',
            'created_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at']


class UserDetailSerializer(UserSerializer):
    """Serializer détaillé avec affectations"""
    affectations = AffectationGareSerializer(many=True, read_only=True)
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['affectations']
