from django.contrib import admin
from .models import DemandeFonds, MembreGare


@admin.register(DemandeFonds)
class DemandeAdmin(admin.ModelAdmin):
    list_display = ['id', 'responsable', 'gare', 'montant', 'statut', 'date_demande']
    list_filter = ['statut', 'date_demande']
    search_fields = ['responsable__nom', 'responsable__prenom', 'gare__nom', 'raison']
    readonly_fields = ['id', 'date_demande']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('id', 'responsable', 'gare', 'montant', 'raison')
        }),
        ('Statut', {
            'fields': ('statut', 'date_demande', 'date_traitement', 'commentaire_admin')
        }),
    )


@admin.register(MembreGare)
class MembreGareAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'gare', 'date_ajout', 'ajout_par', 'est_actif']
    list_filter = ['est_actif', 'date_ajout', 'gare']
    search_fields = ['user__nom', 'user__prenom', 'gare__nom']
    readonly_fields = ['id', 'date_ajout']
    
    fieldsets = (
        ('Association', {
            'fields': ('id', 'user', 'gare', 'est_actif')
        }),
        ('Informations', {
            'fields': ('date_ajout', 'ajout_par')
        }),
    )
