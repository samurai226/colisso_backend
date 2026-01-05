"""
Commande pour charger les colis de test
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.parcels.models import Colis, Livraison, HistoriqueEtat
from apps.users.models import User
from apps.locations.models import Gare


class Command(BaseCommand):
    help = 'Charge les colis de test (7 colis + 6 livraisons)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des colis...')
        
        # Récupérer les users et gares
        expediteur1 = User.objects.filter(telephone='+22670444444').first()
        expediteur2 = User.objects.filter(telephone='+22670555555').first()
        
        colissiers = User.objects.filter(role__nom='colissier')
        livreurs = User.objects.filter(role__nom='livreur')
        
        gare_tampouy = Gare.objects.filter(nom='Tampouy').first()
        gare_gounghin = Gare.objects.filter(nom='Gounghin').first()
        gare_pissy = Gare.objects.filter(nom='Pissy').first()
        gare_bobo = Gare.objects.filter(nom='Bobo-Dioulasso').first()
        
        if not all([expediteur1, gare_tampouy, gare_bobo]):
            self.stdout.write(self.style.ERROR('Données manquantes (users ou gares)'))
            return
        
        # Créer 7 colis avec différents statuts
        colis_data = [
            # 1. Colis en attente
            {
                'code_suivi': 'COL-TEST001',
                'description': 'Vêtements et chaussures',
                'poids': 5.5,
                'valeur_declaree': 50000,
                'expediteur': expediteur1,
                'destinataire_nom': 'KONE Mariam',
                'destinataire_telephone': '+22678111111',
                'destinataire_adresse': 'Quartier Gounghin, Rue 12.34',
                'gare_depart': gare_tampouy,
                'gare_arrivee': gare_gounghin,
                'statut': Colis.EN_ATTENTE,
                'prix': 2500,
                'montant_paye': 2500,
            },
            # 2. Colis en cours
            {
                'code_suivi': 'COL-TEST002',
                'description': 'Matériel électronique',
                'poids': 3.2,
                'valeur_declaree': 200000,
                'expediteur': expediteur1,
                'destinataire_nom': 'SAWADOGO Ali',
                'destinataire_telephone': '+22678222222',
                'destinataire_adresse': 'Quartier Pissy, Avenue de la paix',
                'gare_depart': gare_tampouy,
                'gare_arrivee': gare_pissy,
                'statut': Colis.EN_COURS,
                'prix': 3500,
                'montant_paye': 3500,
            },
            # 3. Colis arrivé
            {
                'code_suivi': 'COL-TEST003',
                'description': 'Documents et livres',
                'poids': 2.0,
                'valeur_declaree': 10000,
                'expediteur': expediteur2,
                'destinataire_nom': 'TRAORE Fatou',
                'destinataire_telephone': '+22678333333',
                'destinataire_adresse': 'Accart-Ville, Rue 5',
                'gare_depart': gare_tampouy,
                'gare_arrivee': gare_bobo,
                'statut': Colis.ARRIVE,
                'prix': 5000,
                'montant_paye': 5000,
                'date_arrivee_reelle': timezone.now(),
            },
            # 4. Colis en livraison
            {
                'code_suivi': 'COL-TEST004',
                'description': 'Produits alimentaires',
                'poids': 10.0,
                'valeur_declaree': 25000,
                'expediteur': expediteur1,
                'destinataire_nom': 'OUEDRAOGO Paul',
                'destinataire_telephone': '+22678444444',
                'destinataire_adresse': 'Quartier Tampouy, Rue 7.15',
                'gare_depart': gare_gounghin,
                'gare_arrivee': gare_tampouy,
                'statut': Colis.EN_LIVRAISON,
                'prix': 4000,
                'montant_paye': 4000,
            },
            # 5. Colis livré
            {
                'code_suivi': 'COL-TEST005',
                'description': 'Pièces détachées moto',
                'poids': 7.5,
                'valeur_declaree': 80000,
                'expediteur': expediteur2,
                'destinataire_nom': 'KABORE Jean',
                'destinataire_telephone': '+22678555555',
                'destinataire_adresse': 'Quartier Pissy, Rue 3.21',
                'gare_depart': gare_tampouy,
                'gare_arrivee': gare_pissy,
                'statut': Colis.LIVRE,
                'prix': 6000,
                'montant_paye': 6000,
                'date_arrivee_reelle': timezone.now() - timedelta(days=1),
                'date_livraison': timezone.now(),
            },
            # 6. Colis avec problème
            {
                'code_suivi': 'COL-TEST006',
                'description': 'Colis fragile - Vaisselle',
                'poids': 4.0,
                'valeur_declaree': 30000,
                'expediteur': expediteur1,
                'destinataire_nom': 'ZONGO Sophie',
                'destinataire_telephone': '+22678666666',
                'destinataire_adresse': 'Quartier Gounghin, Avenue 12',
                'gare_depart': gare_tampouy,
                'gare_arrivee': gare_gounghin,
                'statut': Colis.PROBLEME,
                'prix': 3000,
                'montant_paye': 3000,
            },
            # 7. Colis annulé
            {
                'code_suivi': 'COL-TEST007',
                'description': 'Colis urgent',
                'poids': 1.5,
                'valeur_declaree': 15000,
                'expediteur': expediteur2,
                'destinataire_nom': 'ILBOUDO Michel',
                'destinataire_telephone': '+22678777777',
                'destinataire_adresse': 'Quartier Tampouy, Rue 2.08',
                'gare_depart': gare_pissy,
                'gare_arrivee': gare_tampouy,
                'statut': Colis.ANNULE,
                'prix': 2000,
                'montant_paye': 0,
            },
        ]
        
        colis_crees = []
        for data in colis_data:
            colis, created = Colis.objects.get_or_create(
                code_suivi=data['code_suivi'],
                defaults=data
            )
            
            if created:
                colis_crees.append(colis)
                self.stdout.write(f'  + Colis: {colis.code_suivi} - {colis.get_statut_display()}')
                
                # Créer l'historique initial
                HistoriqueEtat.objects.create(
                    colis=colis,
                    ancien_statut=None,
                    nouveau_statut=colis.statut,
                    commentaire=f"Colis créé - {colis.get_statut_display()}",
                    localisation=colis.gare_depart
                )
        
        self.stdout.write(f'✓ Colis créés: {len(colis_crees)}')
        
        # Créer des livraisons
        if livreurs.exists():
            livraisons_data = [
                # Livraison en attente
                {
                    'colis_code': 'COL-TEST003',
                    'statut': Livraison.EN_ATTENTE,
                },
                # Livraison assignée
                {
                    'colis_code': 'COL-TEST003',
                    'livreur': livreurs[0],
                    'statut': Livraison.ASSIGNEE,
                    'date_assignation': timezone.now() - timedelta(hours=2),
                },
                # Livraison en cours
                {
                    'colis_code': 'COL-TEST004',
                    'livreur': livreurs[0] if livreurs.count() > 0 else None,
                    'statut': Livraison.EN_COURS,
                    'date_assignation': timezone.now() - timedelta(hours=3),
                    'date_debut': timezone.now() - timedelta(hours=1),
                },
                # Livraison livrée
                {
                    'colis_code': 'COL-TEST005',
                    'livreur': livreurs[1] if livreurs.count() > 1 else livreurs[0],
                    'statut': Livraison.LIVREE,
                    'date_assignation': timezone.now() - timedelta(days=1, hours=5),
                    'date_debut': timezone.now() - timedelta(days=1, hours=2),
                    'date_fin': timezone.now(),
                    'signature_destinataire': 'Signature_Base64',
                    'commentaire_livreur': 'Livraison réussie',
                },
                # Livraison avec échec
                {
                    'colis_code': 'COL-TEST006',
                    'livreur': livreurs[2] if livreurs.count() > 2 else livreurs[0],
                    'statut': Livraison.ECHEC,
                    'date_assignation': timezone.now() - timedelta(hours=6),
                    'date_debut': timezone.now() - timedelta(hours=4),
                    'date_fin': timezone.now() - timedelta(hours=2),
                    'raison_echec': 'Destinataire absent',
                },
            ]
            
            livraisons_creees = 0
            for data in livraisons_data:
                colis_code = data.pop('colis_code')
                colis = Colis.objects.filter(code_suivi=colis_code).first()
                
                if colis:
                    livraison, created = Livraison.objects.get_or_create(
                        colis=colis,
                        defaults=data
                    )
                    
                    if created:
                        livraisons_creees += 1
                        self.stdout.write(f'  + Livraison: {colis.code_suivi} - {livraison.get_statut_display()}')
            
            self.stdout.write(f'✓ Livraisons créées: {livraisons_creees}')
        
        self.stdout.write(self.style.SUCCESS('✓ Parcels chargés avec succès!'))
        self.stdout.write(f'  - {len(colis_crees)} Colis')
        self.stdout.write(f'  - Livraisons créées')
