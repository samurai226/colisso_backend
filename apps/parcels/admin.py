"""
Parcels admin
"""
from django.contrib import admin
from .models import Colis, Livraison, HistoriqueEtat


@admin.register(Colis)
class ColisAdmin(admin.ModelAdmin):
    list_display = [
        'code_suivi', 'expediteur', 'destinataire_nom',
        'gare_depart', 'gare_arrivee', 'statut', 'prix', 'est_paye',
        'date_expedition', 'is_active'
    ]
    list_filter = ['statut', 'gare_depart', 'gare_arrivee', 'is_active', 'date_expedition']
    search_fields = ['code_suivi', 'destinataire_nom', 'destinataire_telephone', 'description']
    ordering = ['-date_expedition']
    date_hierarchy = 'date_expedition'
    readonly_fields = ['code_suivi', 'date_expedition', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('code_suivi', 'description', 'poids', 'valeur_declaree')
        }),
        ('Expéditeur', {
            'fields': ('expediteur',)
        }),
        ('Destinataire', {
            'fields': ('destinataire_nom', 'destinataire_telephone', 'destinataire_adresse')
        }),
        ('Gares', {
            'fields': ('gare_depart', 'gare_arrivee')
        }),
        ('Statut et Prix', {
            'fields': ('statut', 'prix', 'montant_paye')
        }),
        ('Dates', {
            'fields': (
                'date_expedition', 'date_arrivee_prevue',
                'date_arrivee_reelle', 'date_livraison'
            )
        }),
        ('Autres', {
            'fields': ('notes', 'is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Livraison)
class LivraisonAdmin(admin.ModelAdmin):
    list_display = [
        'colis', 'livreur', 'statut',
        'date_assignation', 'date_debut', 'date_fin', 'is_active'
    ]
    list_filter = ['statut', 'is_active', 'date_assignation']
    search_fields = ['colis__code_suivi', 'livreur__nom', 'livreur__prenom']
    ordering = ['-date_assignation']
    date_hierarchy = 'date_assignation'
    autocomplete_fields = ['colis', 'livreur']


@admin.register(HistoriqueEtat)
class HistoriqueEtatAdmin(admin.ModelAdmin):
    list_display = [
        'colis', 'ancien_statut', 'nouveau_statut',
        'utilisateur', 'localisation', 'created_at'
    ]
    list_filter = ['nouveau_statut', 'localisation', 'created_at']
    search_fields = ['colis__code_suivi', 'commentaire']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
