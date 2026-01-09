from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Colonnes affichées dans la liste
    list_display = [
        'telephone',
        'nom',
        'prenom',
        'email',
        'get_role_display',
        'is_active',
        'created_at'
    ]
    
    # Filtres sur le côté
    list_filter = [
        'role',
        'is_active',
        'is_staff',
        'is_superuser',
        'created_at'
    ]
    
    # Recherche
    search_fields = [
        'telephone',
        'nom',
        'prenom',
        'email'
    ]
    
    # Ordre par défaut
    ordering = ['-created_at']
    
    # Nombre d'éléments par page
    list_per_page = 25
    
    # Colonnes cliquables
    list_display_links = ['telephone', 'nom']
    
    # Colonnes éditables directement
    list_editable = ['is_active']
    
    # Actions personnalisées
    actions = ['activate_users', 'deactivate_users', 'make_staff']
    
    def get_role_display(self, obj):
        """Afficher le rôle avec un badge coloré"""
        if obj.role:
            colors = {
                'Admin': 'danger',
                'Gerant': 'warning',
                'Guichetier': 'info',
                'Livreur': 'success',
                'Client': 'primary',
            }
            color = colors.get(obj.role.nom, 'secondary')
            return f'<span class="badge badge-{color}">{obj.role.nom}</span>'
        return '-'
    get_role_display.short_description = 'Rôle'
    get_role_display.allow_tags = True
    
    # Actions personnalisées
    @admin.action(description='✅ Activer les utilisateurs sélectionnés')
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} utilisateur(s) activé(s) avec succès.')
    
    @admin.action(description='❌ Désactiver les utilisateurs sélectionnés')
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} utilisateur(s) désactivé(s) avec succès.')
    
    @admin.action(description='👤 Promouvoir en staff')
    def make_staff(self, request, queryset):
        updated = queryset.update(is_staff=True)
        self.message_user(request, f'{updated} utilisateur(s) promu(s) en staff.')
    
    # Organisation des champs dans le formulaire
    fieldsets = (
        ('📱 Informations de connexion', {
            'fields': ('telephone', 'password')
        }),
        ('👤 Informations personnelles', {
            'fields': ('nom', 'prenom', 'email')
        }),
        ('👔 Rôle et permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('📅 Dates importantes', {
            'fields': ('last_login', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('📱 Créer un nouvel utilisateur', {
            'classes': ('wide',),
            'fields': ('telephone', 'nom', 'prenom', 'email', 'password1', 'password2', 'role', 'is_active'),
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login']
    
    # Permissions
    def has_delete_permission(self, request, obj=None):
        # Seul le superuser peut supprimer
        return request.user.is_superuser