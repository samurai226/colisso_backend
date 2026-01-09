"""
Users admin - Gestion des utilisateurs et affectations
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import Role, User, AffectationGare


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Interface admin pour les rôles"""
    
    list_display = ['nom', 'code', 'description', 'get_status_badge', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['nom', 'code', 'description']
    ordering = ['nom']
    list_per_page = 25
    
    fieldsets = (
        ('👔 Informations du rôle', {
            'fields': ('nom', 'code', 'description')
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
        """Badge coloré pour le statut"""
        if obj.is_active:
            return format_html('<span class="badge badge-success">Actif</span>')
        return format_html('<span class="badge badge-danger">Inactif</span>')
    get_status_badge.short_description = 'Statut'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Interface admin pour les utilisateurs"""
    
    # Colonnes affichées dans la liste
    list_display = [
        'telephone',
        'get_nom_complet',
        'email',
        'get_role_badge',
        'get_status_badge',
        'is_staff',
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
    list_display_links = ['telephone']
    
    # Actions personnalisées
    actions = ['activate_users', 'deactivate_users', 'make_staff', 'remove_staff']
    
    # Organisation des champs dans le formulaire d'édition
    fieldsets = (
        ('📱 Informations de connexion', {
            'fields': ('telephone', 'password')
        }),
        ('👤 Informations personnelles', {
            'fields': ('nom', 'prenom', 'email')
        }),
        ('👔 Rôle et permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('👥 Groupes et permissions', {
            'fields': ('groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('📅 Dates importantes', {
            'fields': ('last_login', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Formulaire pour la création d'un nouvel utilisateur
    add_fieldsets = (
        ('📱 Créer un nouvel utilisateur', {
            'classes': ('wide',),
            'fields': (
                'telephone',
                'nom',
                'prenom',
                'email',
                'role',
                'password1',
                'password2',
                'is_active'
            ),
        }),
    )
    
    # Champs en lecture seule
    readonly_fields = ['created_at', 'updated_at', 'last_login']
    
    # Autocomplete pour les relations
    autocomplete_fields = ['role']
    
    # Méthodes d'affichage personnalisées
    
    def get_nom_complet(self, obj):
        """Afficher le nom complet"""
        return f'{obj.prenom} {obj.nom}' if obj.prenom and obj.nom else obj.telephone
    get_nom_complet.short_description = 'Nom complet'
    
    def get_role_badge(self, obj):
        """Afficher le rôle avec un badge coloré"""
        if obj.role:
            colors = {
                'Admin': 'danger',
                'Gestionnaire': 'warning',
                'Gerant': 'warning',
                'Guichetier': 'info',
                'Cashier': 'info',
                'Livreur': 'success',
                'Client': 'primary',
                'Expediteur': 'secondary',
            }
            color = colors.get(obj.role.nom, 'secondary')
            return format_html(
                '<span class="badge badge-{}">{}</span>',
                color,
                obj.role.nom
            )
        return format_html('<span class="text-muted">-</span>')
    get_role_badge.short_description = 'Rôle'
    
    def get_status_badge(self, obj):
        """Badge coloré pour le statut"""
        if obj.is_active:
            return format_html('<span class="badge badge-success">Actif</span>')
        return format_html('<span class="badge badge-danger">Inactif</span>')
    get_status_badge.short_description = 'Statut'
    
    # Actions personnalisées
    
    @admin.action(description='✅ Activer les utilisateurs sélectionnés')
    def activate_users(self, request, queryset):
        """Activer plusieurs utilisateurs"""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f'{updated} utilisateur(s) activé(s) avec succès.',
            level='success'
        )
    
    @admin.action(description='❌ Désactiver les utilisateurs sélectionnés')
    def deactivate_users(self, request, queryset):
        """Désactiver plusieurs utilisateurs"""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated} utilisateur(s) désactivé(s) avec succès.',
            level='warning'
        )
    
    @admin.action(description='👤 Promouvoir en staff')
    def make_staff(self, request, queryset):
        """Promouvoir des utilisateurs en staff"""
        updated = queryset.update(is_staff=True)
        self.message_user(
            request,
            f'{updated} utilisateur(s) promu(s) en staff.',
            level='info'
        )
    
    @admin.action(description='👥 Retirer le statut staff')
    def remove_staff(self, request, queryset):
        """Retirer le statut staff"""
        # Ne pas retirer le staff du superuser actuel
        queryset = queryset.exclude(id=request.user.id)
        updated = queryset.update(is_staff=False)
        self.message_user(
            request,
            f'{updated} utilisateur(s) retiré(s) du staff.',
            level='info'
        )
    
    # Permissions
    
    def has_delete_permission(self, request, obj=None):
        """Seul le superuser peut supprimer des utilisateurs"""
        return request.user.is_superuser


@admin.register(AffectationGare)
class AffectationGareAdmin(admin.ModelAdmin):
    """Interface admin pour les affectations de gares"""
    
    list_display = [
        'user',
        'gare',
        'get_ville',
        'date_debut',
        'date_fin',
        'get_principale_badge',
        'get_status_badge'
    ]
    
    list_filter = [
        'gare__quartier__ville',
        'est_principale',
        'is_active',
        'date_debut'
    ]
    
    search_fields = [
        'user__nom',
        'user__prenom',
        'user__telephone',
        'gare__nom',
        'gare__quartier__ville__nom'
    ]
    
    ordering = ['-date_debut']
    date_hierarchy = 'date_debut'
    list_per_page = 25
    autocomplete_fields = ['user', 'gare']
    
    # ✅ FIELDSETS CORRIGÉ
    fieldsets = (
        ('Utilisateur et gare', {
            'fields': ('user', 'gare')
        }),
        ('Periode affectation', {
            'fields': ('date_debut', 'date_fin')
        }),
        ('Configuration', {
            'fields': ('est_principale', 'is_active')
        }),
        ('Metadonnees', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    actions = ['activer_affectations', 'desactiver_affectations', 'marquer_principale']
    
    # Méthodes d'affichage
    def get_ville(self, obj):
        """Afficher la ville de la gare"""
        if obj.gare and obj.gare.quartier and obj.gare.quartier.ville:
            return obj.gare.quartier.ville.nom
        return '-'
    get_ville.short_description = 'Ville'
    
    def get_principale_badge(self, obj):
        """Badge pour affectation principale"""
        if obj.est_principale:
            return format_html('<span class="badge badge-primary">Principale</span>')
        return format_html('<span class="badge badge-secondary">Secondaire</span>')
    get_principale_badge.short_description = 'Type'
    
    def get_status_badge(self, obj):
        """Badge coloré pour le statut"""
        if obj.is_active:
            return format_html('<span class="badge badge-success">Active</span>')
        return format_html('<span class="badge badge-danger">Inactive</span>')
    get_status_badge.short_description = 'Statut'
    
    # Actions personnalisées
    @admin.action(description='Activer les affectations')
    def activer_affectations(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} affectation(s) activee(s).')
    
    @admin.action(description='Desactiver les affectations')
    def desactiver_affectations(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} affectation(s) desactivee(s).')
    
    @admin.action(description='Marquer comme principale')
    def marquer_principale(self, request, queryset):
        updated = queryset.update(est_principale=True)
        self.message_user(request, f'{updated} affectation(s) marquee(s) comme principale.')
    
    # Permissions
    def has_delete_permission(self, request, obj=None):
        """Seul le superuser peut supprimer des affectations"""
        return request.user.is_superuser