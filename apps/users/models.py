"""
Users models - User, Role, AffectationGare
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from apps.core.models import BaseModel


class Role(BaseModel):
    """
    Rôle utilisateur
    """
    ADMIN = 'admin'
    GERANT = 'gerant'
    GUICHETIER = 'guichetier'
    COLISSIER = 'colissier'
    LIVREUR = 'livreur'
    CLIENT = 'client'
    EXPEDITEUR = 'expediteur'
    
    ROLE_CHOICES = [
        (ADMIN, 'Administrateur'),
        (GERANT, 'Gérant'),
        (GUICHETIER, 'Guichetier'),
        (COLISSIER, 'Colissier'),
        (LIVREUR, 'Livreur'),
        (CLIENT, 'Client'),
        (EXPEDITEUR, 'Expéditeur/Récepteur'),
    ]
    
    nom = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        unique=True,
        verbose_name="Nom du rôle"
    )
    description = models.TextField(blank=True, verbose_name="Description")
    
    class Meta:
        verbose_name = "Rôle"
        verbose_name_plural = "Rôles"
        ordering = ['nom']
    
    def __str__(self):
        return self.get_nom_display()


class UserManager(BaseUserManager):
    """
    Custom user manager
    """
    def create_user(self, telephone, password=None, **extra_fields):
        if not telephone:
            raise ValueError('Le numéro de téléphone est obligatoire')
        
        user = self.model(telephone=telephone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, telephone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(telephone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    Utilisateur personnalisé avec authentification par téléphone
    """
    telephone = PhoneNumberField(
        unique=True,
        verbose_name="Numéro de téléphone"
    )
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name='users',
        null=True,
        blank=True,
        verbose_name="Rôle"
    )
    
    # Django required fields
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['nom', 'prenom']
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.telephone})"
    
    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"


class AffectationGare(BaseModel):
    """
    Affectation d'un utilisateur à une gare
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='affectations',
        verbose_name="Utilisateur"
    )
    gare = models.ForeignKey(
        'locations.Gare',
        on_delete=models.CASCADE,
        related_name='affectations',
        verbose_name="Gare"
    )
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de fin"
    )
    est_principale = models.BooleanField(
        default=False,
        verbose_name="Gare principale"
    )
    
    class Meta:
        verbose_name = "Affectation à une gare"
        verbose_name_plural = "Affectations aux gares"
        ordering = ['-date_debut']
        unique_together = ['user', 'gare', 'date_debut']
    
    def __str__(self):
        return f"{self.user.nom_complet} → {self.gare.nom}"
