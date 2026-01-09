from django.contrib import admin
from .models import Pays, Ville, Quartier, Gare

@admin.register(Pays)
class PaysAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code', 'indicatif', 'is_active']
    list_filter = ['is_active']
    search_fields = ['nom', 'code']

@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'pays', 'is_active']
    list_filter = ['pays', 'is_active']
    search_fields = ['nom']

@admin.register(Quartier)
class QuartierAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ville', 'is_active']
    list_filter = ['ville', 'is_active']
    search_fields = ['nom']

@admin.register(Gare)
class GareAdmin(admin.ModelAdmin):
    list_display = ['nom', 'quartier', 'is_active']
    list_filter = ['quartier__ville', 'is_active']
    search_fields = ['nom', 'adresse']