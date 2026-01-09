"""
Trips admin
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Trajet, Reservation


@admin.register(Trajet)
class TrajetAdmin(admin.ModelAdmin):
    list_display = [
        'get_trajet_display',
        'date_depart',
        'heure_depart',
        'prix_base',
        'get_places_display',
        'statut',
        'type_trajet'
    ]
    
    list_filter = ['statut', 'type_trajet', 'is_vip', 'date_depart']
    search_fields = ['ville_depart', 'ville_arrivee', 'compagnie_nom']
    date_hierarchy = 'date_depart'
    ordering = ['-date_depart', '-heure_depart']
    
    readonly_fields = ['created_at', 'updated_at', 'taux_occupation', 'places_disponibles']
    
    def get_trajet_display(self, obj):
        return format_html('<strong>{}</strong> → <strong>{}</strong>', obj.ville_depart, obj.ville_arrivee)
    get_trajet_display.short_description = 'Trajet'
    
    def get_places_display(self, obj):
        return f'{obj.places_disponibles} / {obj.capacite_max}'
    get_places_display.short_description = 'Places dispo'


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        'numero_ticket',
        'get_client_display',
        'numero_siege',
        'statut',
        'montant_paye',
        'date_reservation'
    ]
    
    list_filter = ['statut', 'date_reservation']
    search_fields = ['numero_ticket', 'client_nom', 'client_prenom', 'client_telephone']
    date_hierarchy = 'date_reservation'
    ordering = ['-date_reservation']
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_client_display(self, obj):
        return f'{obj.client_prenom} {obj.client_nom}'
    get_client_display.short_description = 'Client'
    
    actions = ['valider_reservations', 'annuler_reservations']
    
    @admin.action(description='Valider')
    def valider_reservations(self, request, queryset):
        for res in queryset:
            res.valider()
    
    @admin.action(description='Annuler')
    def annuler_reservations(self, request, queryset):
        queryset.update(statut='annulee')