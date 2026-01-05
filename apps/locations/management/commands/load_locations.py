"""
Commande pour charger les données de locations (Burkina Faso)
"""
from django.core.management.base import BaseCommand
from apps.locations.models import Pays, Ville, Quartier, Gare


class Command(BaseCommand):
    help = 'Charge les données de locations (Burkina Faso avec 4 gares)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des locations...')
        
        # 1. Créer le pays
        burkina, _ = Pays.objects.get_or_create(
            code='BF',
            defaults={
                'nom': 'Burkina Faso',
                'indicatif': '+226'
            }
        )
        self.stdout.write(f'✓ Pays: {burkina.nom}')
        
        # 2. Créer les villes
        villes_data = [
            {'nom': 'Ouagadougou', 'population': 2415266},
            {'nom': 'Bobo-Dioulasso', 'population': 903887},
            {'nom': 'Koudougou', 'population': 131825},
            {'nom': 'Ouahigouya', 'population': 124587},
        ]
        
        villes = {}
        for ville_data in villes_data:
            ville, _ = Ville.objects.get_or_create(
                nom=ville_data['nom'],
                pays=burkina,
                defaults={'population': ville_data['population']}
            )
            villes[ville.nom] = ville
        
        self.stdout.write(f'✓ Villes: {len(villes)}')
        
        # 3. Créer les quartiers
        quartiers_data = [
            # Ouagadougou
            {'nom': 'Tampouy', 'ville': 'Ouagadougou'},
            {'nom': 'Gounghin', 'ville': 'Ouagadougou'},
            {'nom': 'Pissy', 'ville': 'Ouagadougou'},
            {'nom': 'Tanghin', 'ville': 'Ouagadougou'},
            # Bobo-Dioulasso
            {'nom': 'Accart-Ville', 'ville': 'Bobo-Dioulasso'},
            {'nom': 'Hamdalaye', 'ville': 'Bobo-Dioulasso'},
            # Koudougou
            {'nom': 'Centre', 'ville': 'Koudougou'},
            # Ouahigouya
            {'nom': 'Centre', 'ville': 'Ouahigouya'},
        ]
        
        quartiers = {}
        for quartier_data in quartiers_data:
            ville = villes[quartier_data['ville']]
            quartier, _ = Quartier.objects.get_or_create(
                nom=quartier_data['nom'],
                ville=ville
            )
            quartiers[f"{quartier.nom}-{ville.nom}"] = quartier
        
        self.stdout.write(f'✓ Quartiers: {len(quartiers)}')
        
        # 4. Créer les 4 gares principales
        gares_data = [
            {
                'nom': 'Tampouy',
                'quartier': 'Tampouy-Ouagadougou',
                'adresse': 'Avenue Charles de Gaulle, Tampouy',
                'telephone': '+22625301234',
                'latitude': 12.3714,
                'longitude': -1.5197,
            },
            {
                'nom': 'Gounghin',
                'quartier': 'Gounghin-Ouagadougou',
                'adresse': 'Route de Kaya, Gounghin',
                'telephone': '+22625302345',
                'latitude': 12.3854,
                'longitude': -1.5104,
            },
            {
                'nom': 'Pissy',
                'quartier': 'Pissy-Ouagadougou',
                'adresse': 'Boulevard de la Révolution, Pissy',
                'telephone': '+22625303456',
                'latitude': 12.3512,
                'longitude': -1.5378,
            },
            {
                'nom': 'Bobo-Dioulasso',
                'quartier': 'Accart-Ville-Bobo-Dioulasso',
                'adresse': 'Avenue de la Nation, Accart-Ville',
                'telephone': '+22620971234',
                'latitude': 11.1770,
                'longitude': -4.2979,
            },
        ]
        
        for gare_data in gares_data:
            quartier_key = gare_data.pop('quartier')
            quartier = quartiers[quartier_key]
            
            gare, created = Gare.objects.get_or_create(
                nom=gare_data['nom'],
                quartier=quartier,
                defaults={
                    'adresse': gare_data['adresse'],
                    'telephone': gare_data['telephone'],
                    'latitude': gare_data['latitude'],
                    'longitude': gare_data['longitude'],
                }
            )
            
            if created:
                self.stdout.write(f'  + Gare {gare.nom}')
        
        self.stdout.write(self.style.SUCCESS('✓ Locations chargées avec succès!'))
        self.stdout.write(f'  - 1 Pays')
        self.stdout.write(f'  - {len(villes)} Villes')
        self.stdout.write(f'  - {len(quartiers)} Quartiers')
        self.stdout.write(f'  - 4 Gares')
