"""
Commande pour charger les utilisateurs de test
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.users.models import Role, User, AffectationGare
from apps.locations.models import Gare


class Command(BaseCommand):
    help = 'Charge les utilisateurs de test (17 users)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des utilisateurs...')
        
        # 1. Créer les rôles
        roles_data = [
            {'nom': Role.ADMIN, 'description': 'Administrateur système'},
            {'nom': Role.GERANT, 'description': 'Gérant de gare'},
            {'nom': Role.GUICHETIER, 'description': 'Agent guichet'},
            {'nom': Role.COLISSIER, 'description': 'Gestionnaire de colis'},
            {'nom': Role.LIVREUR, 'description': 'Livreur'},
            {'nom': Role.CLIENT, 'description': 'Client'},
            {'nom': Role.EXPEDITEUR, 'description': 'Expéditeur/Récepteur'},
        ]
        
        roles = {}
        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                nom=role_data['nom'],
                defaults={'description': role_data['description']}
            )
            roles[role.nom] = role
            if created:
                self.stdout.write(f'  + Rôle: {role.get_nom_display()}')
        
        self.stdout.write(f'✓ Rôles: {len(roles)}')
        
        # 2. Récupérer les gares
        gares = {
            'tampouy': Gare.objects.filter(nom='Tampouy').first(),
            'gounghin': Gare.objects.filter(nom='Gounghin').first(),
            'pissy': Gare.objects.filter(nom='Pissy').first(),
            'bobo': Gare.objects.filter(nom='Bobo-Dioulasso').first(),
        }
        
        # 3. Créer les utilisateurs
        users_data = [
            # Admin (1)
            {
                'telephone': '+22670000001',
                'nom': 'ADMIN',
                'prenom': 'Super',
                'role': Role.ADMIN,
                'password': 'admin123',
                'is_staff': True,
                'is_superuser': True,
            },
            # Gérants (2)
            {
                'telephone': '+22670000010',
                'nom': 'OUEDRAOGO',
                'prenom': 'Jean',
                'role': Role.GERANT,
                'password': 'gerant123',
                'gare': 'tampouy',
            },
            {
                'telephone': '+22670000011',
                'nom': 'KABORE',
                'prenom': 'Marie',
                'role': Role.GERANT,
                'password': 'gerant123',
                'gare': 'bobo',
            },
            # Guichetiers (2)
            {
                'telephone': '+22670000020',
                'nom': 'SAWADOGO',
                'prenom': 'Paul',
                'role': Role.GUICHETIER,
                'password': 'guichet123',
                'gare': 'tampouy',
            },
            {
                'telephone': '+22670000021',
                'nom': 'ZOUNGRANA',
                'prenom': 'Aïcha',
                'role': Role.GUICHETIER,
                'password': 'guichet123',
                'gare': 'gounghin',
            },
            # Colissiers (3)
            {
                'telephone': '+22670000030',
                'nom': 'COMPAORE',
                'prenom': 'Amadou',
                'role': Role.COLISSIER,
                'password': 'colis123',
                'gare': 'tampouy',
            },
            {
                'telephone': '+22670000031',
                'nom': 'TRAORE',
                'prenom': 'Fatou',
                'role': Role.COLISSIER,
                'password': 'colis123',
                'gare': 'pissy',
            },
            {
                'telephone': '+22670000032',
                'nom': 'SANOGO',
                'prenom': 'Ibrahim',
                'role': Role.COLISSIER,
                'password': 'colis123',
                'gare': 'bobo',
            },
            # Livreurs (4)
            {
                'telephone': '+22670000040',
                'nom': 'KONATE',
                'prenom': 'Moussa',
                'role': Role.LIVREUR,
                'password': 'livreur123',
                'gare': 'tampouy',
            },
            {
                'telephone': '+22670000041',
                'nom': 'DIARRA',
                'prenom': 'Seydou',
                'role': Role.LIVREUR,
                'password': 'livreur123',
                'gare': 'gounghin',
            },
            {
                'telephone': '+22670000042',
                'nom': 'COULIBALY',
                'prenom': 'Lassane',
                'role': Role.LIVREUR,
                'password': 'livreur123',
                'gare': 'pissy',
            },
            {
                'telephone': '+22670000043',
                'nom': 'TOURE',
                'prenom': 'Souleymane',
                'role': Role.LIVREUR,
                'password': 'livreur123',
                'gare': 'bobo',
            },
            # Clients (3)
            {
                'telephone': '+22670111111',
                'nom': 'ZONGO',
                'prenom': 'Aminata',
                'role': Role.CLIENT,
                'password': 'client123',
            },
            {
                'telephone': '+22670222222',
                'nom': 'YAMEOGO',
                'prenom': 'Clarisse',
                'role': Role.CLIENT,
                'password': 'client123',
            },
            {
                'telephone': '+22670333333',
                'nom': 'NIKIEMA',
                'prenom': 'Michel',
                'role': Role.CLIENT,
                'password': 'client123',
            },
            # Expéditeurs (2)
            {
                'telephone': '+22670444444',
                'nom': 'BARRO',
                'prenom': 'Sophie',
                'role': Role.EXPEDITEUR,
                'password': 'expediteur123',
            },
            {
                'telephone': '+22670555555',
                'nom': 'ILBOUDO',
                'prenom': 'Jacques',
                'role': Role.EXPEDITEUR,
                'password': 'expediteur123',
            },
        ]
        
        created_count = 0
        for user_data in users_data:
            gare_key = user_data.pop('gare', None)
            password = user_data.pop('password')
            role_code = user_data.pop('role')
            
            user, created = User.objects.get_or_create(
                telephone=user_data['telephone'],
                defaults={
                    **user_data,
                    'role': roles[role_code]
                }
            )
            
            if created:
                user.set_password(password)
                user.save()
                created_count += 1
                self.stdout.write(f'  + User: {user.nom_complet} ({user.telephone})')
                
                # Affecter à une gare si nécessaire
                if gare_key and gares.get(gare_key):
                    AffectationGare.objects.get_or_create(
                        user=user,
                        gare=gares[gare_key],
                        defaults={
                            'date_debut': timezone.now().date(),
                            'est_principale': True,
                        }
                    )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Utilisateurs créés: {created_count}'))
        self.stdout.write(f'  Total: {User.objects.count()} utilisateurs')
