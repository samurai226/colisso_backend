from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        'numero',
        'client',
        'trajet',
        'nombre_places',
        'get_statut_badge',
        'created_at'
    ]
    
    list_filter = ['statut', 'created_at', 'trajet__gare_depart']
    search_fields = ['numero', 'client__nom', 'client__prenom']
    date_hierarchy = 'created_at'
    
    actions = ['valider_reservations', 'annuler_reservations']
    
    fieldsets = (
        ('🎫 Réservation', {
            'fields': ('numero', 'client', 'trajet', 'nombre_places')
        }),
        ('💰 Paiement', {
            'fields': ('montant', 'statut')
        }),
        ('📅 Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['numero', 'created_at', 'updated_at']
    
    def get_statut_badge(self, obj):
        colors = {
            'EN_ATTENTE': 'warning',
            'CONFIRMEE': 'success',
            'ANNULEE': 'danger',
            'TERMINEE': 'info',
        }
        color = colors.get(obj.statut, 'secondary')
        return f'<span class="badge badge-{color}">{obj.get_statut_display()}</span>'
    get_statut_badge.short_description = 'Statut'
    get_statut_badge.allow_tags = True
    
    @admin.action(description='✅ Valider les réservations')
    def valider_reservations(self, request, queryset):
        updated = queryset.update(statut='CONFIRMEE')
        self.message_user(request, f'{updated} réservation(s) validée(s).')
    
    @admin.action(description='❌ Annuler les réservations')
    def annuler_reservations(self, request, queryset):
        updated = queryset.update(statut='ANNULEE')
        self.message_user(request, f'{updated} réservation(s) annulée(s).')