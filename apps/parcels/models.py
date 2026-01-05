"""
Parcels models - Colis, Livraison, HistoriqueEtat
"""
from django.db import models
from apps.core.models import BaseModel


class Colis(BaseModel):
    """
    Colis model - Package/Parcel
    """
    # Statuts possibles
    EN_ATTENTE = 'en_attente'
    EN_COURS = 'en_cours'
    ARRIVE = 'arrive'
    EN_LIVRAISON = 'en_livraison'
    LIVRE = 'livre'
    PROBLEME = 'probleme'
    ANNULE = 'annule'
    
    STATUT_CHOICES = [
        (EN_ATTENTE, 'En attente'),
        (EN_COURS, 'En cours de transport'),
        (ARRIVE, 'Arrivé à destination'),
        (EN_LIVRAISON, 'En cours de livraison'),
        (LIVRE, 'Livré'),
        (PROBLEME, 'Problème'),
        (ANNULE, 'Annulé'),
    ]
    
    # Informations de base
    code_suivi = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Code de suivi"
    )
    description = models.TextField(verbose_name="Description du contenu")
    poids = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Poids (kg)"
    )
    valeur_declaree = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Valeur déclarée (FCFA)"
    )
    
    # Expéditeur et destinataire
    expediteur = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='colis_expedies',
        verbose_name="Expéditeur"
    )
    destinataire_nom = models.CharField(
        max_length=200,
        verbose_name="Nom du destinataire"
    )
    destinataire_telephone = models.CharField(
        max_length=20,
        verbose_name="Téléphone destinataire"
    )
    destinataire_adresse = models.TextField(
        verbose_name="Adresse destinataire"
    )
    
    # Gares
    gare_depart = models.ForeignKey(
        'locations.Gare',
        on_delete=models.PROTECT,
        related_name='colis_departs',
        verbose_name="Gare de départ"
    )
    gare_arrivee = models.ForeignKey(
        'locations.Gare',
        on_delete=models.PROTECT,
        related_name='colis_arrivees',
        verbose_name="Gare d'arrivée"
    )
    
    # Statut et prix
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default=EN_ATTENTE,
        verbose_name="Statut"
    )
    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix (FCFA)"
    )
    montant_paye = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Montant payé (FCFA)"
    )
    
    # Dates
    date_expedition = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'expédition"
    )
    date_arrivee_prevue = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date d'arrivée prévue"
    )
    date_arrivee_reelle = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date d'arrivée réelle"
    )
    date_livraison = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de livraison"
    )
    
    # Notes
    notes = models.TextField(
        blank=True,
        verbose_name="Notes internes"
    )
    
    class Meta:
        verbose_name = "Colis"
        verbose_name_plural = "Colis"
        ordering = ['-date_expedition']
    
    def __str__(self):
        return f"{self.code_suivi} - {self.get_statut_display()}"
    
    @property
    def est_paye(self):
        """Vérifie si le colis est entièrement payé"""
        return self.montant_paye >= self.prix


class Livraison(BaseModel):
    """
    Livraison model - Delivery
    """
    # Statuts de livraison
    EN_ATTENTE = 'en_attente'
    ASSIGNEE = 'assignee'
    EN_COURS = 'en_cours'
    LIVREE = 'livree'
    ECHEC = 'echec'
    
    STATUT_CHOICES = [
        (EN_ATTENTE, 'En attente'),
        (ASSIGNEE, 'Assignée'),
        (EN_COURS, 'En cours'),
        (LIVREE, 'Livrée'),
        (ECHEC, 'Échec'),
    ]
    
    colis = models.ForeignKey(
        Colis,
        on_delete=models.CASCADE,
        related_name='livraisons',
        verbose_name="Colis"
    )
    livreur = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='livraisons',
        null=True,
        blank=True,
        verbose_name="Livreur"
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default=EN_ATTENTE,
        verbose_name="Statut"
    )
    
    # Dates
    date_assignation = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date d'assignation"
    )
    date_debut = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de début"
    )
    date_fin = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de fin"
    )
    
    # Preuve de livraison
    signature_destinataire = models.TextField(
        blank=True,
        verbose_name="Signature destinataire (base64)"
    )
    photo_livraison = models.URLField(
        blank=True,
        verbose_name="Photo de livraison"
    )
    commentaire_livreur = models.TextField(
        blank=True,
        verbose_name="Commentaire du livreur"
    )
    
    # En cas d'échec
    raison_echec = models.TextField(
        blank=True,
        verbose_name="Raison de l'échec"
    )
    
    class Meta:
        verbose_name = "Livraison"
        verbose_name_plural = "Livraisons"
        ordering = ['-created_at']
    
    def __str__(self):
        livreur_nom = self.livreur.nom_complet if self.livreur else "Non assigné"
        return f"Livraison {self.colis.code_suivi} - {livreur_nom}"


class HistoriqueEtat(BaseModel):
    """
    Historique des changements d'état d'un colis
    """
    colis = models.ForeignKey(
        Colis,
        on_delete=models.CASCADE,
        related_name='historique',
        verbose_name="Colis"
    )
    ancien_statut = models.CharField(
        max_length=20,
        choices=Colis.STATUT_CHOICES,
        null=True,
        blank=True,
        verbose_name="Ancien statut"
    )
    nouveau_statut = models.CharField(
        max_length=20,
        choices=Colis.STATUT_CHOICES,
        verbose_name="Nouveau statut"
    )
    utilisateur = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='historique_modifications',
        verbose_name="Utilisateur"
    )
    commentaire = models.TextField(
        blank=True,
        verbose_name="Commentaire"
    )
    localisation = models.ForeignKey(
        'locations.Gare',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Localisation"
    )
    
    class Meta:
        verbose_name = "Historique d'état"
        verbose_name_plural = "Historiques d'état"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.colis.code_suivi} - {self.get_nouveau_statut_display()}"
