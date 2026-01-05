import uuid
from django.db import models
from django.utils import timezone


class Trajet(models.Model):
    """Modèle pour les trajets de bus"""
    
    STATUS_CHOICES = [
        ('planifie', 'Planifié'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
    ]
    
    TYPE_CHOICES = [
        ('ordinaire', 'Ordinaire'),
        ('vip', 'VIP'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Informations du trajet
    ville_depart = models.CharField(max_length=100, verbose_name="Ville de départ")
    ville_arrivee = models.CharField(max_length=100, verbose_name="Ville d'arrivée")
    
    # Horaires et durée
    date_depart = models.DateField(verbose_name="Date de départ")
    heure_depart = models.TimeField(verbose_name="Heure de départ")
    duree_estimee = models.IntegerField(help_text="Durée en minutes", verbose_name="Durée estimée")
    
    # Tarification
    prix_base = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix de base")
    
    # Capacité
    capacite_max = models.IntegerField(verbose_name="Capacité maximale")
    places_reservees = models.IntegerField(default=0, verbose_name="Places réservées")
    
    # Type et statut
    type_trajet = models.CharField(
        max_length=20, 
        choices=TYPE_CHOICES, 
        default='ordinaire',
        verbose_name="Type de trajet"
    )
    is_vip = models.BooleanField(default=False, verbose_name="Trajet VIP")
    statut = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='planifie',
        verbose_name="Statut"
    )
    
    # Informations complémentaires
    compagnie_nom = models.CharField(max_length=100, blank=True, verbose_name="Nom de la compagnie")
    bus_immatriculation = models.CharField(max_length=50, blank=True, verbose_name="Immatriculation du bus")
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    
    class Meta:
        db_table = 'trips_trajet'
        verbose_name = 'Trajet'
        verbose_name_plural = 'Trajets'
        ordering = ['-date_depart', '-heure_depart']
    
    def __str__(self):
        return f"{self.ville_depart} → {self.ville_arrivee} ({self.date_depart} {self.heure_depart})"
    
    @property
    def places_disponibles(self):
        """Calcule les places disponibles"""
        return self.capacite_max - self.places_reservees
    
    @property
    def is_complet(self):
        """Vérifie si le trajet est complet"""
        return self.places_reservees >= self.capacite_max
    
    @property
    def taux_occupation(self):
        """Calcule le taux d'occupation en %"""
        if self.capacite_max == 0:
            return 0
        return round((self.places_reservees / self.capacite_max) * 100, 2)


class Reservation(models.Model):
    """Modèle pour les réservations de trajets"""
    
    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('payee', 'Payée'),
        ('validee', 'Validée'),
        ('annulee', 'Annulée'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relations
    trajet_id = models.UUIDField(verbose_name="ID du trajet")
    client_telephone = models.CharField(max_length=20, verbose_name="Téléphone du client")
    
    # Informations du client
    client_nom = models.CharField(max_length=100, verbose_name="Nom du client")
    client_prenom = models.CharField(max_length=100, verbose_name="Prénom du client")
    client_email = models.EmailField(blank=True, null=True, verbose_name="Email du client")
    
    # Réservation
    numero_ticket = models.CharField(max_length=50, unique=True, verbose_name="Numéro de ticket")
    numero_siege = models.IntegerField(verbose_name="Numéro de siège")
    
    # Statut et paiement
    statut = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='en_attente',
        verbose_name="Statut"
    )
    montant_paye = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        verbose_name="Montant payé"
    )
    
    # Métadonnées
    date_reservation = models.DateTimeField(default=timezone.now, verbose_name="Date de réservation")
    date_validation = models.DateTimeField(null=True, blank=True, verbose_name="Date de validation")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    
    class Meta:
        db_table = 'trips_reservation'
        verbose_name = 'Réservation'
        verbose_name_plural = 'Réservations'
        ordering = ['-date_reservation']
        unique_together = [['trajet_id', 'numero_siege']]
    
    def __str__(self):
        return f"Ticket {self.numero_ticket} - {self.client_nom} {self.client_prenom}"
    
    @property
    def is_payee(self):
        """Vérifie si la réservation est payée"""
        return self.statut in ['payee', 'validee']
    
    @property
    def is_validee(self):
        """Vérifie si la réservation est validée"""
        return self.statut == 'validee'
    
    def valider(self):
        """Valide la réservation"""
        self.statut = 'validee'
        self.date_validation = timezone.now()
        self.save()
