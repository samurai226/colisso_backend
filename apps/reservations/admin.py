"""
Reservations admin
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    # Liste des colonnes affichées
    list_display = [
        'numero_ticket',
        'client',
        'get_trajet_display',
        'prix',
        'get_statut_badge',
        'date_reservation'
    ]
    
    # Filtres sur le côté
    list_filter = ['statut', 'date_reservation', 'trajet__gare_depart__quartier__ville']
    
    # Recherche
    search_fields = [
        'numero_ticket',
        'client__nom',
        'client__prenom',
        'client__telephone'
    ]
    
    # Hiérarchie de dates
    date_hierarchy = 'date_reservation'
    
    # Ordre par défaut
    ordering = ['-date_reservation']
    
    # Nombre par page
    list_per_page = 25
    
    # Actions personnalisées
    actions = ['valider_reservations', 'annuler_reservations']
    
    # Organisation des champs dans le formulaire
    fieldsets = (
        ('🎫 Informations du ticket', {
            'fields': ('numero_ticket', 'client', 'trajet', 'prix')
        }),
        ('📊 Statut', {
            'fields': ('statut',)
        }),
        ('📅 Dates', {
            'fields': ('date_reservation', 'date_validation', 'valide_par')
        }),
    )
    
    # Champs en lecture seule
    readonly_fields = ['numero_ticket', 'date_reservation']
    
    # Autocomplete pour les relations
    autocomplete_fields = ['client', 'trajet']
    
    # Méthodes personnalisées pour l'affichage
    
    def get_trajet_display(self, obj):
        """Afficher le trajet de manière lisible"""
        if obj.trajet:
            depart = obj.trajet.gare_depart.nom if obj.trajet.gare_depart else '?'
            arrivee = obj.trajet.gare_arrivee.nom if obj.trajet.gare_arrivee else '?'
            return f'{depart} → {arrivee}'
        return '-'
    get_trajet_display.short_description = 'Trajet'
    
    def get_statut_badge(self, obj):
        """Afficher le statut avec un badge coloré"""
        statut_colors = {
            'EN_ATTENTE': ('warning', 'En attente'),
            'CONFIRMEE': ('success', 'Confirmée'),
            'VALIDEE': ('success', 'Validée'),
            'ANNULEE': ('danger', 'Annulée'),
            'TERMINEE': ('info', 'Terminée'),
        }
        
        color, label = statut_colors.get(obj.statut, ('secondary', obj.statut))
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            color,
            label
        )
    get_statut_badge.short_description = 'Statut'
    
    # Actions personnalisées
    
    @admin.action(description='✅ Valider les réservations sélectionnées')
    def valider_reservations(self, request, queryset):
        """Marquer les réservations comme confirmées"""
        updated = queryset.update(
            statut='CONFIRMEE',
            valide_par=request.user
        )
        self.message_user(
            request,
            f'{updated} réservation(s) validée(s) avec succès.',
            level='success'
        )
    
    @admin.action(description='❌ Annuler les réservations sélectionnées')
    def annuler_reservations(self, request, queryset):
        """Marquer les réservations comme annulées"""
        updated = queryset.update(statut='ANNULEE')
        self.message_user(
            request,
            f'{updated} réservation(s) annulée(s) avec succès.',
            level='warning'
        )
    
    # Personnalisation de l'affichage
    
    def has_delete_permission(self, request, obj=None):
        """Seul le superuser peut supprimer des réservations"""
        return request.user.is_superuser
    
    class Meta:
        verbose_name = 'Réservation'
        verbose_name_plural = 'Réservations'