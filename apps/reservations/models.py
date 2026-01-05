from django.db import models
from apps.users.models import User
from apps.trips.models import Trajet
import uuid


class Reservation(models.Model):
    """Réservation/Ticket pour un trajet"""
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
        ('valide', 'Validé'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero_ticket = models.CharField(max_length=50, unique=True, editable=False)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE, related_name='reservations')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    date_reservation = models.DateTimeField(auto_now_add=True)
    date_validation = models.DateTimeField(null=True, blank=True)
    valide_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_valides')
    
    class Meta:
        db_table = 'reservations'
        ordering = ['-date_reservation']
        
    def __str__(self):
        return f"Ticket {self.numero_ticket} - {self.client.nomComplet}"
    
    def save(self, *args, **kwargs):
        # Générer numéro de ticket si nouveau
        if not self.numero_ticket:
            import random
            import string
            self.numero_ticket = f"TK{''.join(random.choices(string.digits, k=6))}"
        super().save(*args, **kwargs)
