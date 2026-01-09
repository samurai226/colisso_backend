from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['numero_ticket', 'client_nom', 'client_prenom', 'statut']
    list_filter = ['statut']
    search_fields = ['numero_ticket', 'client_nom', 'client_prenom']
    
    actions = ['valider_reservations', 'annuler_reservations']
    
    @admin.action(description='Valider')
    def valider_reservations(self, request, queryset):
        queryset.update(statut='validee')
    
    @admin.action(description='Annuler')
    def annuler_reservations(self, request, queryset):
        queryset.update(statut='annulee')