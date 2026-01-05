"""
Core models - Base model for all other models
"""
from django.db import models
from django.utils import timezone
import uuid


class BaseModel(models.Model):
    """
    Base model with common fields for all models
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )
    
    class Meta:
        abstract = True
        ordering = ['-created_at']
    
    def __str__(self):
        return str(self.id)
    
    def soft_delete(self):
        """Soft delete: mark as inactive instead of deleting"""
        self.is_active = False
        self.save()
    
    def restore(self):
        """Restore a soft-deleted object"""
        self.is_active = True
        self.save()
