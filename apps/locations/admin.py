"""
Locations admin
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Pays, Ville, Quartier, Gare


@admin.register(Pays)
class PaysAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code', 'indicatif', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['nom', 'code', 'indicatif']
    ordering = ['nom']


@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'pays', 'population', 'is_active', 'created_at']
    list_filter = ['pays', 'is_active', 'created_at']
    search_fields = ['nom', 'pays__nom']
    ordering = ['nom']


@admin.register(Quartier)
class QuartierAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ville', 'is_active', 'created_at']
    list_filter = ['ville__pays', 'ville', 'is_active', 'created_at']
    search_fields = ['nom', 'ville__nom']
    ordering = ['nom']


@admin.register(Gare)
class GareAdmin(admin.ModelAdmin):
    list_display = ['nom', 'quartier', 'get_ville', 'telephone', 'is_active', 'created_at']
    list_filter = ['quartier__ville__pays', 'quartier__ville', 'is_active', 'created_at']
    search_fields = ['nom', 'adresse', 'quartier__nom', 'quartier__ville__nom']
    ordering = ['nom']
    
    def get_ville(self, obj):
        return obj.ville.nom if obj.ville else '-'
    get_ville.short_description = 'Ville'