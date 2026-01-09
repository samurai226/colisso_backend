from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Role, User, AffectationGare

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code', 'is_active']
    list_filter = ['is_active']
    search_fields = ['nom', 'code']

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['telephone', 'nom', 'prenom', 'is_active']
    list_filter = ['is_active', 'is_staff']
    search_fields = ['telephone', 'nom', 'prenom']
    ordering = ['telephone']
    
    fieldsets = (
        (None, {'fields': ('telephone', 'password')}),
        ('Infos', {'fields': ('nom', 'prenom')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    
    add_fieldsets = (
        (None, {
            'fields': ('telephone', 'nom', 'prenom', 'password1', 'password2'),
        }),
    )

@admin.register(AffectationGare)
class AffectationGareAdmin(admin.ModelAdmin):
    list_display = ['user', 'gare', 'est_principale', 'is_active']
    list_filter = ['est_principale', 'is_active']
    search_fields = ['user__nom', 'gare__nom']