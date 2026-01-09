from django.contrib import admin
from .models import Trajet, Reservation

@admin.register(Trajet)
class TrajetAdmin(admin.ModelAdmin):
    list_display = ['ville_depart', 'ville_arrivee', 'date_depart', 'statut']
    list_filter = ['statut', 'date_depart']
    search_fields = ['ville_depart', 'ville_arrivee']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['numero_ticket', 'client_nom', 'statut']
    list_filter = ['statut']
    search_fields = ['numero_ticket', 'client_nom']