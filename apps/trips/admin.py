"""
Trips admin - Gestion des trajets et réservations
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Trajet, Reservation


@admin.register(Trajet)
class TrajetAdmin(admin.ModelAdmin):
    """Interface admin pour les trajets"""
    
    # Colonnes affichées
    list_display = [
        'get_trajet_display',
        'date_depart',
        'heure_depart',
        'prix_base',
        'get_places_display',
        'get_statut_badge',
        'type_trajet',
    ]
    
    # Filtres
    list_filter = [
        'statut',
        'type_trajet',
        'is_vip',
        'date_depart',
        'ville_depart',
        'ville_arrivee',
    ]
    
    # Recherche
    search_fields = [
        'ville_depart',
        'ville_arrivee',
        'compagnie_nom',
        'bus_immatriculation',
    ]
    
    # Hiérarchie de dates
    date_hierarchy = 'date_depart'
    
    # Ordre par défaut
    ordering = ['-date_depart', 'heure_depart']
    
    # Nombre par page
    list_per_page = 25
    
    # Champs en lecture seule
    readonly_fields = ['id', 'created_at', 'updated_at', 'taux_occupation', 'places_reservees']
    
    # Organisation des champs
    fieldsets = (
        ('🚌 Informations du trajet', {
            'fields': (
                'id',
                'ville_depart',
                'ville_arrivee',
            )
        }),
        ('⏰ Horaires', {
            'fields': (
                'date_depart',
                'heure_depart',
                'duree_estimee',
            )
        }),
        ('💰 Tarification', {
            'fields': (
                'prix_base',
                'is_vip',
            )
        }),
        ('🎫 Capacité', {
            'fields': (
                'capacite_max',
                'places_reservees',
                'taux_occupation',
            )
        }),
        ('📊 Statut et type', {
            'fields': (
                'type_trajet',
                'statut',
            )
        }),
        ('🚍 Informations complémentaires', {
            'fields': (
                'compagnie_nom',
                'bus_immatriculation',
            ),
            'classes': ('collapse',)
        }),
        ('📅 Métadonnées', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    # Actions personnalisées
    actions = ['activer_trajets', 'annuler_trajets']
    
    # Méthodes d'affichage personnalisées
    
    def get_trajet_display(self, obj):
        """Afficher le trajet de manière lisible"""
        return format_html(
            '<strong>{}</strong> → <strong>{}</strong>',
            obj.ville_depart,
            obj.ville_arrivee
        )
    get_trajet_display.short_description = 'Trajet'
    
    def get_places_display(self, obj):
        """Afficher les places disponibles"""
        places_dispo = obj.capacite_max - obj.places_reservees
        
        if places_dispo > 10:
            color = 'success'
        elif places_dispo > 0:
            color = 'warning'
        else:
            color = 'danger'
        
        return format_html(
            '<span class="badge badge-{}">{} / {}</span>',
            color,
            places_dispo,
            obj.capacite_max
        )
    get_places_display.short_description = 'Places disponibles'
    
    def get_statut_badge(self, obj):
        """Badge coloré pour le statut"""
        statut_colors = {
            'actif': ('success', 'Actif'),
            'complet': ('danger', 'Complet'),
            'annule': ('secondary', 'Annulé'),
            'termine': ('info', 'Terminé'),
        }
        
        color, label = statut_colors.get(obj.statut, ('secondary', obj.statut))
        return format_html('<span class="badge badge-{}">{}</span>', color, label)
    get_statut_badge.short_description = 'Statut'
    
    # Actions personnalisées
    
    @admin.action(description='✅ Activer les trajets sélectionnés')
    def activer_trajets(self, request, queryset):
        updated = queryset.update(statut='actif')
        self.message_user(request, f'{updated} trajet(s) activé(s).')
    
    @admin.action(description='❌ Annuler les trajets sélectionnés')
    def annuler_trajets(self, request, queryset):
        updated = queryset.update(statut='annule')
        self.message_user(request, f'{updated} trajet(s) annulé(s).')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Interface admin pour les réservations"""
    
    # Colonnes affichées
    list_display = [
        'numero_ticket',
        'get_client_display',
        'get_trajet_display',
        'numero_siege',
        'get_statut_badge',
        'montant_paye',
        'date_reservation',
    ]
    
    # Filtres
    list_filter = [
        'statut',
        'date_reservation',
        'date_validation',
    ]
    
    # Recherche
    search_fields = [
        'numero_ticket',
        'client_nom',
        'client_prenom',
        'client_telephone',
        'client_email',
    ]
    
    # Hiérarchie de dates
    date_hierarchy = 'date_reservation'
    
    # Ordre par défaut
    ordering = ['-date_reservation']
    
    # Nombre par page
    list_per_page = 25
    
    # Champs en lecture seule
    readonly_fields = ['id', 'numero_ticket', 'created_at', 'updated_at']
    
    # Organisation des champs
    fieldsets = (
        ('🎫 Identification', {
            'fields': (
                'id',
                'numero_ticket',
                'trajet_id',
            )
        }),
        ('👤 Informations du client', {
            'fields': (
                'client_nom',
                'client_prenom',
                'client_telephone',
                'client_email',
            )
        }),
        ('📋 Détails de la réservation', {
            'fields': (
                'numero_siege',
                'statut',
                'montant_paye',
            )
        }),
        ('📅 Dates', {
            'fields': (
                'date_reservation',
                'date_validation',
            )
        }),
        ('📊 Métadonnées', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    # Actions personnalisées
    actions = ['valider_reservations', 'annuler_reservations']
    
    # Méthodes d'affichage personnalisées
    
    def get_client_display(self, obj):
        """Afficher le nom complet du client"""
        return f'{obj.client_prenom} {obj.client_nom}'
    get_client_display.short_description = 'Client'
    
    def get_trajet_display(self, obj):
        """Afficher le trajet lié"""
        if obj.trajet_id:
            try:
                trajet = Trajet.objects.get(id=obj.trajet_id)
                return format_html(
                    '{} → {}',
                    trajet.ville_depart,
                    trajet.ville_arrivee
                )
            except Trajet.DoesNotExist:
                return format_html('<span class="text-muted">Trajet #{}</span>', obj.trajet_id)
        return '-'
    get_trajet_display.short_description = 'Trajet'
    
    def get_statut_badge(self, obj):
        """Badge coloré pour le statut"""
        statut_colors = {
            'en_attente': ('warning', 'En attente'),
            'confirmee': ('info', 'Confirmée'),
            'validee': ('success', 'Validée'),
            'annulee': ('danger', 'Annulée'),
        }
        
        color, label = statut_colors.get(obj.statut, ('secondary', obj.statut))
        return format_html('<span class="badge badge-{}">{}</span>', color, label)
    get_statut_badge.short_description = 'Statut'
    
    # Actions personnalisées
    
    @admin.action(description='✅ Valider les réservations sélectionnées')
    def valider_reservations(self, request, queryset):
        """Valider plusieurs réservations"""
        count = 0
        for reservation in queryset:
            if hasattr(reservation, 'is_validee'):
                if not reservation.is_validee and reservation.statut != 'annulee':
                    if hasattr(reservation, 'valider'):
                        reservation.valider()
                    else:
                        reservation.statut = 'validee'
                        reservation.save()
                    count += 1
            else:
                # Si pas de méthode is_validee, update direct
                if reservation.statut in ['en_attente', 'confirmee']:
                    reservation.statut = 'validee'
                    reservation.save()
                    count += 1
        
        self.message_user(
            request,
            f'{count} réservation(s) validée(s) avec succès.',
            level='success'
        )
    
    @admin.action(description='❌ Annuler les réservations sélectionnées')
    def annuler_reservations(self, request, queryset):
        """Annuler plusieurs réservations"""
        count = queryset.filter(
            statut__in=['en_attente', 'confirmee']
        ).update(statut='annulee')
        
        self.message_user(
            request,
            f'{count} réservation(s) annulée(s) avec succès.',
            level='warning'
        )
    
    # Permissions
    
    def has_delete_permission(self, request, obj=None):
        """Seul le superuser peut supprimer des réservations"""
        return request.user.is_superuser