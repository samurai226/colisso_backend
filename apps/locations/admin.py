"""
Locations admin
"""
from django.contrib import admin
from .models import Pays, Ville, Quartier, Gare


@admin.register(Pays)
class PaysAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code', 'indicatif', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['nom', 'code']
    ordering = ['nom']


@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'pays', 'population', 'is_active', 'created_at']
    list_filter = ['pays', 'is_active']
    search_fields = ['nom']
    ordering = ['nom']
    autocomplete_fields = ['pays']


@admin.register(Quartier)
class QuartierAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ville', 'is_active', 'created_at']
    list_filter = ['ville__pays', 'ville', 'is_active']
    search_fields = ['nom', 'ville__nom']
    ordering = ['nom']
    autocomplete_fields = ['ville']


@admin.register(Gare)
class GareAdmin(admin.ModelAdmin):
    list_display = ['nom', 'quartier', 'ville_display', 'telephone', 'is_active', 'created_at']
    list_filter = ['quartier__ville__pays', 'quartier__ville', 'is_active']
    search_fields = ['nom', 'adresse', 'quartier__nom']
    ordering = ['nom']
    autocomplete_fields = ['quartier']
    
    def ville_display(self, obj):
        return obj.quartier.ville.nom
    ville_display.short_description = 'Ville'
