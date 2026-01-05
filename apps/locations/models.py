"""
Locations models - Pays, Ville, Quartier, Gare
"""
from django.db import models
from apps.core.models import BaseModel


class Pays(BaseModel):
    """
    Pays (Country) model
    """
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    code = models.CharField(max_length=3, unique=True, verbose_name="Code ISO")
    indicatif = models.CharField(max_length=10, verbose_name="Indicatif téléphonique")
    
    class Meta:
        verbose_name = "Pays"
        verbose_name_plural = "Pays"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class Ville(BaseModel):
    """
    Ville (City) model
    """
    nom = models.CharField(max_length=100, verbose_name="Nom")
    pays = models.ForeignKey(
        Pays,
        on_delete=models.CASCADE,
        related_name='villes',
        verbose_name="Pays"
    )
    population = models.IntegerField(null=True, blank=True, verbose_name="Population")
    
    class Meta:
        verbose_name = "Ville"
        verbose_name_plural = "Villes"
        ordering = ['nom']
        unique_together = ['nom', 'pays']
    
    def __str__(self):
        return f"{self.nom}, {self.pays.nom}"


class Quartier(BaseModel):
    """
    Quartier (District) model
    """
    nom = models.CharField(max_length=100, verbose_name="Nom")
    ville = models.ForeignKey(
        Ville,
        on_delete=models.CASCADE,
        related_name='quartiers',
        verbose_name="Ville"
    )
    
    class Meta:
        verbose_name = "Quartier"
        verbose_name_plural = "Quartiers"
        ordering = ['nom']
        unique_together = ['nom', 'ville']
    
    def __str__(self):
        return f"{self.nom}, {self.ville.nom}"


class Gare(BaseModel):
    """
    Gare (Station) model
    """
    nom = models.CharField(max_length=100, verbose_name="Nom")
    quartier = models.ForeignKey(
        Quartier,
        on_delete=models.CASCADE,
        related_name='gares',
        verbose_name="Quartier"
    )
    adresse = models.TextField(verbose_name="Adresse")
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    
    # Coordonnées GPS
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Latitude"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Longitude"
    )
    
    class Meta:
        verbose_name = "Gare"
        verbose_name_plural = "Gares"
        ordering = ['nom']
    
    def __str__(self):
        return f"Gare {self.nom}"
    
    @property
    def ville(self):
        """Raccourci pour accéder à la ville"""
        return self.quartier.ville
    
    @property
    def pays(self):
        """Raccourci pour accéder au pays"""
        return self.quartier.ville.pays
