from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['numero_ticket', 'client', 'trajet', 'statut', 'prix', 'date_reservation']
    list_filter = ['statut', 'date_reservation']
    search_fields = ['numero_ticket', 'client__nom', 'client__prenom']
    readonly_fields = ['id', 'numero_ticket', 'date_reservation']
    
    fieldsets = (
        ('Ticket', {
            'fields': ('id', 'numero_ticket', 'client', 'trajet', 'prix')
        }),
        ('Statut', {
            'fields': ('statut', 'date_reservation', 'date_validation', 'valide_par')
        }),
    )
