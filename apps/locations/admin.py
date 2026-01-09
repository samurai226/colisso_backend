"""
Locations admin
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Pays, Ville, Quartier, Gare


@admin.register(Pays)
class PaysAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code', 'indicatif', 'get_status_badge', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['nom', 'code', 'indicatif']
    ordering = ['nom']
    list_per_page = 25
    
    fieldsets = (
        ('🌍 Informations du pays', {
            'fields': ('nom', 'code', 'indicatif')
        }),
        ('⚙️ Statut', {
            'fields': ('is_active',)
        }),
        ('📅 Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_status_badge(self, obj):
        if obj.is_active:
            return format_html('<span class="badge badge-success">Actif</span>')
        return format_html('<span class="badge badge-danger">Inactif</span>')
    get_status_badge.short_description = 'Statut'


@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'pays', 'get_population_display', 'get_gares_count', 'get_status_badge', 'created_at']
    list_filter = ['pays', 'is_active', 'created_at']
    search_fields = ['nom', 'pays__nom']
    ordering = ['pays', 'nom']
    autocomplete_fields = ['pays']
    list_per_page = 25
    
    fieldsets = (
        ('🏙️ Informations de la ville', {
            'fields': ('nom', 'pays', 'population')
        }),
        ('⚙️ Statut', {
            'fields': ('is_active',)
        }),
        ('📅 Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_population_display(self, obj):
        if obj.population:
            return f'{obj.population:,}'
        return '-'
    get_population_display.short_description = 'Population'
    
    def get_gares_count(self, obj):
        # Compte les gares via Quartier
        count = Gare.objects.filter(quartier__ville=obj).count()
        if count > 0:
            return format_html('<span class="badge badge-info">{} gare(s)</span>', count)
        return format_html('<span class="badge badge-secondary">0</span>')
    get_gares_count.short_description = 'Gares'
    
    def get_status_badge(self, obj):
        if obj.is_active:
            return format_html('<span class="badge badge-success">Actif</span>')
        return format_html('<span class="badge badge-danger">Inactif</span>')
    get_status_badge.short_description = 'Statut'


@admin.register(Quartier)
class QuartierAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ville', 'get_pays', 'get_gares_count', 'get_status_badge', 'created_at']
    list_filter = ['ville__pays', 'ville', 'is_active', 'created_at']
    search_fields = ['nom', 'ville__nom', 'ville__pays__nom']
    ordering = ['ville', 'nom']
    autocomplete_fields = ['ville']
    list_per_page = 25
    
    fieldsets = (
        ('🏘️ Informations du quartier', {
            'fields': ('nom', 'ville')
        }),
        ('⚙️ Statut', {
            'fields': ('is_active',)
        }),
        ('📅 Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_pays(self, obj):
        return obj.ville.pays.nom if obj.ville and obj.ville.pays else '-'
    get_pays.short_description = 'Pays'
    
    def get_gares_count(self, obj):
        count = obj.gares.count()
        if count > 0:
            return format_html('<span class="badge badge-info">{} gare(s)</span>', count)
        return format_html('<span class="badge badge-secondary">0</span>')
    get_gares_count.short_description = 'Gares'
    
    def get_status_badge(self, obj):
        if obj.is_active:
            return format_html('<span class="badge badge-success">Actif</span>')
        return format_html('<span class="badge badge-danger">Inactif</span>')
    get_status_badge.short_description = 'Statut'


@admin.register(Gare)
class GareAdmin(admin.ModelAdmin):
    list_display = ['nom', 'quartier', 'get_ville', 'get_pays', 'telephone', 'get_status_badge', 'created_at']
    list_filter = ['quartier__ville__pays', 'quartier__ville', 'is_active', 'created_at']
    search_fields = ['nom', 'adresse', 'quartier__nom', 'quartier__ville__nom', 'telephone']
    ordering = ['quartier__ville', 'nom']
    autocomplete_fields = ['quartier']
    list_per_page = 25
    
    fieldsets = (
        ('🏢 Informations générales', {
            'fields': ('nom', 'quartier', 'adresse')
        }),
        ('📞 Contact', {
            'fields': ('telephone', 'email')
        }),
        ('⚙️ Statut', {
            'fields': ('is_active',)
        }),
        ('📅 Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_ville(self, obj):
        return obj.quartier.ville.nom if obj.quartier and obj.quartier.ville else '-'
    get_ville.short_description = 'Ville'
    
    def get_pays(self, obj):
        if obj.quartier and obj.quartier.ville and obj.quartier.ville.pays:
            return obj.quartier.ville.pays.nom
        return '-'
    get_pays.short_description = 'Pays'
    
    def get_status_badge(self, obj):
        if obj.is_active:
            return format_html('<span class="badge badge-success">Active</span>')
        return format_html('<span class="badge badge-danger">Inactive</span>')
    get_status_badge.short_description = 'Statut'
    
    # Actions personnalisées
    actions = ['activer_gares', 'desactiver_gares']
    
    @admin.action(description='✅ Activer les gares sélectionnées')
    def activer_gares(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} gare(s) activée(s) avec succès.')
    
    @admin.action(description='❌ Désactiver les gares sélectionnées')
    def desactiver_gares(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} gare(s) désactivée(s) avec succès.')