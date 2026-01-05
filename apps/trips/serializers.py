from rest_framework import serializers
from .models import Trajet, Reservation


class TrajetSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Trajet"""
    
    places_disponibles = serializers.ReadOnlyField()
    is_complet = serializers.ReadOnlyField()
    taux_occupation = serializers.ReadOnlyField()
    
    class Meta:
        model = Trajet
        fields = [
            'id',
            'ville_depart',
            'ville_arrivee',
            'date_depart',
            'heure_depart',
            'duree_estimee',
            'prix_base',
            'capacite_max',
            'places_reservees',
            'places_disponibles',
            'type_trajet',
            'is_vip',
            'statut',
            'compagnie_nom',
            'bus_immatriculation',
            'is_complet',
            'taux_occupation',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'places_disponibles', 'is_complet', 'taux_occupation']


class TrajetListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des trajets"""
    
    places_disponibles = serializers.ReadOnlyField()
    
    class Meta:
        model = Trajet
        fields = [
            'id',
            'ville_depart',
            'ville_arrivee',
            'date_depart',
            'heure_depart',
            'duree_estimee',
            'prix_base',
            'places_disponibles',
            'capacite_max',
            'is_vip',
            'statut',
        ]


class ReservationSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Reservation"""
    
    is_payee = serializers.ReadOnlyField()
    is_validee = serializers.ReadOnlyField()
    
    class Meta:
        model = Reservation
        fields = [
            'id',
            'trajet_id',
            'client_telephone',
            'client_nom',
            'client_prenom',
            'client_email',
            'numero_ticket',
            'numero_siege',
            'statut',
            'montant_paye',
            'date_reservation',
            'date_validation',
            'is_payee',
            'is_validee',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_payee', 'is_validee']
    
    def validate_numero_ticket(self, value):
        """Valide l'unicité du numéro de ticket"""
        if self.instance is None:  # Création
            if Reservation.objects.filter(numero_ticket=value).exists():
                raise serializers.ValidationError("Ce numéro de ticket existe déjà.")
        return value
    
    def validate_numero_siege(self, value):
        """Valide que le numéro de siège est valide"""
        if value < 1:
            raise serializers.ValidationError("Le numéro de siège doit être supérieur à 0.")
        return value


class ReservationListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des réservations"""
    
    class Meta:
        model = Reservation
        fields = [
            'id',
            'trajet_id',
            'client_nom',
            'client_prenom',
            'numero_ticket',
            'numero_siege',
            'statut',
            'date_reservation',
        ]


class ValidationReservationSerializer(serializers.Serializer):
    """Serializer pour la validation d'une réservation"""
    
    numero_ticket = serializers.CharField(max_length=50)
    
    def validate_numero_ticket(self, value):
        """Valide que le ticket existe"""
        try:
            reservation = Reservation.objects.get(numero_ticket=value)
            if reservation.is_validee:
                raise serializers.ValidationError("Ce ticket a déjà été validé.")
            if reservation.statut == 'annulee':
                raise serializers.ValidationError("Ce ticket a été annulé.")
        except Reservation.DoesNotExist:
            raise serializers.ValidationError("Ticket non trouvé.")
        return value
