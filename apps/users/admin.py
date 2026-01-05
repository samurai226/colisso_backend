"""
Users admin
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Role, User, AffectationGare


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'description', 'is_active', 'created_at']
    list_filter = ['nom', 'is_active']
    search_fields = ['nom', 'description']
    ordering = ['nom']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['telephone', 'nom', 'prenom', 'role', 'is_staff', 'is_active', 'created_at']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['telephone', 'nom', 'prenom']
    ordering = ['nom']
    
    fieldsets = (
        (None, {'fields': ('telephone', 'password')}),
        ('Informations personnelles', {'fields': ('nom', 'prenom', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('telephone', 'nom', 'prenom', 'role', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(AffectationGare)
class AffectationGareAdmin(admin.ModelAdmin):
    list_display = ['user', 'gare', 'date_debut', 'date_fin', 'est_principale', 'is_active']
    list_filter = ['gare', 'est_principale', 'is_active']
    search_fields = ['user__nom', 'user__prenom', 'gare__nom']
    ordering = ['-date_debut']
    autocomplete_fields = ['user', 'gare']
    date_hierarchy = 'date_debut'
