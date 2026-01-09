"""
Users admin
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import Role, User, AffectationGare


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'description', 'is_active', 'created_at']
    list_filter = ['nom', 'is_active', 'created_at']
    search_fields = ['nom', 'description']
    ordering = ['nom']
    
    def get_status_badge(self, obj):
        if obj.is_active:
            return format_html('<span class="badge badge-success">Actif</span>')
        return format_html('<span class="badge badge-danger">Inactif</span>')
    get_status_badge.short_description = 'Statut'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['telephone', 'get_nom_complet', 'role', 'is_active', 'is_staff', 'created_at']
    list_filter = ['role', 'is_active', 'is_staff', 'is_superuser', 'created_at']
    search_fields = ['telephone', 'nom', 'prenom']
    ordering = ['-created_at']
    list_per_page = 25
    
    fieldsets = (
        ('Connexion', {
            'fields': ('telephone', 'password')
        }),
        ('Infos personnelles', {
            'fields': ('nom', 'prenom', 'role')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Dates', {
            'fields': ('last_login', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('Nouvel utilisateur', {
            'classes': ('wide',),
            'fields': ('telephone', 'nom', 'prenom', 'role', 'password1', 'password2', 'is_active'),
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login']
    
    def get_nom_complet(self, obj):
        return f'{obj.prenom} {obj.nom}'
    get_nom_complet.short_description = 'Nom complet'
    
    actions = ['activate_users', 'deactivate_users']
    
    @admin.action(description='Activer')
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
    
    @admin.action(description='Desactiver')
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(AffectationGare)
class AffectationGareAdmin(admin.ModelAdmin):
    list_display = ['user', 'gare', 'date_debut', 'date_fin', 'est_principale', 'is_active']
    list_filter = ['est_principale', 'is_active', 'date_debut']
    search_fields = ['user__nom', 'user__prenom', 'gare__nom']
    ordering = ['-date_debut']
    date_hierarchy = 'date_debut'