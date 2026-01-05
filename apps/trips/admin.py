from django.contrib import admin
from .models import Trajet, Reservation


@admin.register(Trajet)
class TrajetAdmin(admin.ModelAdmin):
    """Interface admin pour les trajets"""
    
    list_display = [
        'ville_depart',
        'ville_arrivee',
        'date_depart',
        'heure_depart',
        'prix_base',
        'places_reservees',
        'capacite_max',
        'type_trajet',
        'statut',
    ]
    
    list_filter = [
        'statut',
        'type_trajet',
        'is_vip',
        'date_depart',
        'ville_depart',
        'ville_arrivee',
    ]
    
    search_fields = [
        'ville_depart',
        'ville_arrivee',
        'compagnie_nom',
        'bus_immatriculation',
    ]
    
    readonly_fields = ['id', 'created_at', 'updated_at', 'taux_occupation']
    
    fieldsets = (
        ('Informations du trajet', {
            'fields': (
                'id',
                'ville_depart',
                'ville_arrivee',
                'date_depart',
                'heure_depart',
                'duree_estimee',
            )
        }),
        ('Tarification et capacité', {
            'fields': (
                'prix_base',
                'capacite_max',
                'places_reservees',
                'taux_occupation',
            )
        }),
        ('Type et statut', {
            'fields': (
                'type_trajet',
                'is_vip',
                'statut',
            )
        }),
        ('Informations complémentaires', {
            'fields': (
                'compagnie_nom',
                'bus_immatriculation',
            )
        }),
        ('Métadonnées', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Interface admin pour les réservations"""
    
    list_display = [
        'numero_ticket',
        'client_nom',
        'client_prenom',
        'numero_siege',
        'statut',
        'montant_paye',
        'date_reservation',
    ]
    
    list_filter = [
        'statut',
        'date_reservation',
        'date_validation',
    ]
    
    search_fields = [
        'numero_ticket',
        'client_nom',
        'client_prenom',
        'client_telephone',
        'client_email',
    ]
    
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Identification', {
            'fields': (
                'id',
                'numero_ticket',
                'trajet_id',
            )
        }),
        ('Informations du client', {
            'fields': (
                'client_nom',
                'client_prenom',
                'client_telephone',
                'client_email',
            )
        }),
        ('Réservation', {
            'fields': (
                'numero_siege',
                'statut',
                'montant_paye',
                'date_reservation',
                'date_validation',
            )
        }),
        ('Métadonnées', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['valider_reservations', 'annuler_reservations']
    
    def valider_reservations(self, request, queryset):
        """Action pour valider plusieurs réservations"""
        count = 0
        for reservation in queryset:
            if not reservation.is_validee and reservation.statut != 'annulee':
                reservation.valider()
                count += 1
        
        self.message_user(
            request,
            f"{count} réservation(s) validée(s) avec succès."
        )
    valider_reservations.short_description = "Valider les réservations sélectionnées"
    
    def annuler_reservations(self, request, queryset):
        """Action pour annuler plusieurs réservations"""
        count = 0
        for reservation in queryset.filter(statut__in=['en_attente', 'confirmee']):
            reservation.statut = 'annulee'
            reservation.save()
            count += 1
        
        self.message_user(
            request,
            f"{count} réservation(s) annulée(s) avec succès."
        )
    annuler_reservations.short_description = "Annuler les réservations sélectionnées"
