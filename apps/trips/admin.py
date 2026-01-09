from django.contrib import admin
from .models import Trajet

@admin.register(Trajet)
class TrajetAdmin(admin.ModelAdmin):
    list_display = [
        'get_trajet_display',
        'date_depart',
        'heure_depart',
        'prix',
        'places_disponibles',
        'get_status_badge'
    ]
    
    list_filter = ['gare_depart', 'gare_arrivee', 'date_depart']
    search_fields = ['gare_depart__nom', 'gare_arrivee__nom']
    date_hierarchy = 'date_depart'
    
    fieldsets = (
        ('🚌 Trajet', {
            'fields': ('gare_depart', 'gare_arrivee')
        }),
        ('⏰ Horaires', {
            'fields': ('date_depart', 'heure_depart', 'duree')
        }),
        ('💰 Tarification', {
            'fields': ('prix',)
        }),
        ('🎫 Places', {
            'fields': ('places_totales', 'places_disponibles')
        }),
    )
    
    def get_trajet_display(self, obj):
        return f'{obj.gare_depart.nom} → {obj.gare_arrivee.nom}'
    get_trajet_display.short_description = 'Trajet'
    
    def get_status_badge(self, obj):
        if obj.places_disponibles > 10:
            return '<span class="badge badge-success">Disponible</span>'
        elif obj.places_disponibles > 0:
            return '<span class="badge badge-warning">Peu de places</span>'
        else:
            return '<span class="badge badge-danger">Complet</span>'
    get_status_badge.short_description = 'Statut'
    get_status_badge.allow_tags = True