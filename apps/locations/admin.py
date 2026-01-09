from django.contrib import admin
from .models import Ville, Gare

@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code_postal', 'get_gares_count', 'created_at']
    search_fields = ['nom', 'code_postal']
    list_filter = ['created_at']
    ordering = ['nom']
    
    def get_gares_count(self, obj):
        count = obj.gares.count()
        return f'{count} gare(s)'
    get_gares_count.short_description = 'Nombre de gares'

@admin.register(Gare)
class GareAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ville', 'adresse', 'get_status', 'created_at']
    list_filter = ['ville', 'created_at']
    search_fields = ['nom', 'adresse', 'ville__nom']
    autocomplete_fields = ['ville']
    
    fieldsets = (
        ('🏢 Informations générales', {
            'fields': ('nom', 'ville', 'adresse')
        }),
        ('📞 Contact', {
            'fields': ('telephone', 'email')
        }),
        ('📅 Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_status(self, obj):
        return '<span class="badge badge-success">Active</span>'
    get_status.short_description = 'Statut'
    get_status.allow_tags = True