"""
Django settings for Colisso project - MODULE 1
"""

import os
import dj_database_url
from decouple import config
from pathlib import Path  
from datetime import timedelta 

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent  # ← AJOUTER


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='your-secret-key-here-change-me')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')
ALLOWED_HOSTS.append('.onrender.com')  # Pour Render


# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'django_filters',
    'drf_spectacular',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',
    'phonenumber_field',
    
    # Local apps
    'apps.core',
    'apps.locations',
    'apps.users',
    'apps.authentication',
    'apps.parcels',
    'apps.trips', 
    'apps.manager',
    'apps.reservations',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# DATABASE - Auto-detection
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    # Production ou PostgreSQL local
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
        )
    }
else:
    # Développement avec SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# CACHES - Auto-détection
REDIS_URL = config('REDIS_URL', default=None)

if REDIS_URL:
    # Production avec Redis
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }
else:
    # Développement sans Redis
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Ouagadougou'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# Spectacular (Swagger)
SPECTACULAR_SETTINGS = {
    'TITLE': 'Colisso API - Module 1',
    'DESCRIPTION': 'API de transport de colis - Module CORE',
    'VERSION': '1.0.0',
}

# CORS
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://localhost:8080',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# ==================== JAZZMIN CONFIGURATION ====================

JAZZMIN_SETTINGS = {
    # ==================== BRANDING ====================
    
    # Titre du site
    "site_title": "Colisso Admin",
    "site_header": "COLISSO",
    "site_brand": "Gestion de Transport",
    "site_logo": None,  # Mettre le chemin vers ton logo si tu en as un
    "login_logo": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    
    # Message de bienvenue sur la page d'accueil
    "welcome_sign": "Bienvenue sur l'administration Colisso",
    
    # Copyright footer
    "copyright": "Colisso Transport © 2024-2025",
    
    # ==================== SEARCH ====================
    
    # Modèles dans la barre de recherche
    "search_model": ["users.User", "locations.Gare", "trips.Trajet"],
    
    # ==================== TOP MENU ====================
    
    # Liens en haut à droite
    "topmenu_links": [
        {"name": "🏠 Accueil", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "📚 API Docs", "url": "/api/schema/swagger-ui/", "new_window": True},
        {"name": "🌐 Site Web", "url": "/", "new_window": True},
    ],
    
    # ==================== USER MENU ====================
    
    # Liens dans le menu utilisateur
    "usermenu_links": [
        {"name": "👤 Mon Profil", "url": "admin:password_change", "icon": "fas fa-user"},
    ],
    
    # ==================== SIDEBAR ====================
    
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    
    # Ordre des apps dans le menu
    "order_with_respect_to": [
        "users",
        "locations",
        "trips",
        "reservations",
        "parcels",
        "manager",
        "auth",
    ],
    
    # ==================== ICONS ====================
    
    # Icônes pour chaque app et modèle
    "icons": {
        # Auth (Django par défaut)
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        
        # Users
        "users": "fas fa-user-circle",
        "users.User": "fas fa-id-card",
        
        # Locations
        "locations": "fas fa-map-marked-alt",
        "locations.Gare": "fas fa-building",
        "locations.Ville": "fas fa-city",
        
        # Trips
        "trips": "fas fa-route",
        "trips.Trajet": "fas fa-road",
        "trips.Bus": "fas fa-bus",
        
        # Reservations
        "reservations": "fas fa-ticket-alt",
        "reservations.Reservation": "fas fa-clipboard-list",
        
        # Parcels
        "parcels": "fas fa-box-open",
        "parcels.Colis": "fas fa-box",
        
        # Manager
        "manager": "fas fa-chart-line",
        "manager.Caisse": "fas fa-cash-register",
        "manager.Statistique": "fas fa-chart-bar",
    },
    
    # Icônes par défaut
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-arrow-circle-right",
    
    # ==================== RELATED MODAL ====================
    
    "related_modal_active": False,
    
    # ==================== CUSTOM CSS/JS ====================
    
    "custom_css": None,
    "custom_js": None,
    
    # ==================== SHOW UI BUILDER ====================
    
    "show_ui_builder": False,
    
    # ==================== CHANGEFORM FORMAT ====================
    
    # Format des formulaires: horizontal_tabs, vertical_tabs, collapsible, carousel
    "changeform_format": "horizontal_tabs",
    
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
        "users.User": "horizontal_tabs",
    },
}

# ==================== UI TWEAKS ====================

JAZZMIN_UI_TWEAKS = {
    # Taille du texte
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    
    # Couleurs principales (Colisso = Bleu)
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    
    # Navbar (barre du haut)
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    
    # Sidebar (menu latéral)
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "sidebar_fixed": True,
    
    # Layout
    "layout_boxed": False,
    "footer_fixed": False,
    
    # Thème général
    "theme": "default",  # Options: default, darkly, solar, superhero, slate
    
    # Classes des boutons
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
}