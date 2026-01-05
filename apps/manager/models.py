from django.db import models
from apps.users.models import User
from apps.locations.models import Gare
import uuid

class DemandeFonds(models.Model):
    """Demande de transfert de fonds par un responsable de gare"""
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('approuvee', 'Approuvée'),
        ('rejetee', 'Rejetée'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    responsable = models.ForeignKey(User, on_delete=models.CASCADE, related_name='demandes_fonds')
    gare = models.ForeignKey(Gare, on_delete=models.CASCADE, related_name='demandes_fonds')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    raison = models.TextField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_demande = models.DateTimeField(auto_now_add=True)
    date_traitement = models.DateTimeField(null=True, blank=True)
    commentaire_admin = models.TextField(blank=True)
    
    class Meta:
        db_table = 'manager_demandes_fonds'
        ordering = ['-date_demande']
        
    def __str__(self):
        return f"Demande {self.montant} FCFA - {self.responsable.nomComplet} - {self.statut}"


class MembreGare(models.Model):
    """Association entre un utilisateur et une gare (pour la gestion des membres)"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gares_associees')
    gare = models.ForeignKey(Gare, on_delete=models.CASCADE, related_name='membres')
    date_ajout = models.DateTimeField(auto_now_add=True)
    ajout_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='membres_ajoutes')
    est_actif = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'manager_membres_gare'
        unique_together = ['user', 'gare']
        ordering = ['-date_ajout']
        
    def __str__(self):
        return f"{self.user.nomComplet} - {self.gare.nom}"
