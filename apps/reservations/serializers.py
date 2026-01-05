from rest_framework import serializers
from .models import Reservation
from apps.users.serializers import UserSerializer
from apps.trips.serializers import TrajetSerializer


class ReservationSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    trajet = TrajetSerializer(read_only=True)
    valide_par_nom = serializers.CharField(source='valide_par.nomComplet', read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'numero_ticket', 'client', 'trajet', 'statut', 'prix',
            'date_reservation', 'date_validation', 'valide_par', 'valide_par_nom'
        ]
        read_only_fields = ['id', 'numero_ticket', 'date_reservation', 'date_validation']


class ReservationCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer une réservation"""
    
    class Meta:
        model = Reservation
        fields = ['trajet', 'prix']
    
    def create(self, validated_data):
        # Le client est l'utilisateur connecté
        validated_data['client'] = self.context['request'].user
        return super().create(validated_data)
