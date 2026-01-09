"""
Reservations admin
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        'numero_ticket',
        'client',
        'trajet',
        'prix',
        'statut',
        'date_reservation'
    ]
    
    list_filter = ['statut', 'date_reservation']
    search_fields = ['numero_ticket', 'client__nom', 'client__prenom', 'client__telephone']
    date_hierarchy = 'date_reservation'
    ordering = ['-date_reservation']
    
    readonly_fields = ['numero_ticket', 'date_reservation']
    
    actions = ['valider_reservations', 'annuler_reservations']
    
    @admin.action(description='Valider')
    def valider_reservations(self, request, queryset):
        queryset.update(statut='valide')
    
    @admin.action(description='Annuler')
    def annuler_reservations(self, request, queryset):
        queryset.update(statut='annule')